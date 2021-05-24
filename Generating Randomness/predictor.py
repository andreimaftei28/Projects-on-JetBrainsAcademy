"""Script for a small game of
guessing the 0's and 1's input typed by a player"""

from itertools import product
import re
import random


def clean_string(strng):
    """Function used for replaceing characters that are different
    from 0 and 1 in a given string"""

    for char in strng:
        if char not in "01":
            strng = strng.replace(char, "")
    return strng

def random_string():
    """Function take's input from user until it reaches at least 100 char"""

    final = ""
    print(f"Please give AI some data to learn...\nCurrent data length is {len(final)}, {100 - len(final)} symbols left")
    while True:
        if len(final) <= 100:
            strng = input("Print a random string containing 0 or 1:\n\n")
            final += clean_string(strng)
            print(f"Current data length is {len(final)}, {100 - len(final)} symbols left")
        else:
            print(f"Final data string:\n{final}\n")
            return final


def analyze(strng):
    """Function for analysing a binary string,
    to predict the next input char. It returns 2 dicts containing
    the frequency of 0 and 1 after a given triad of chars"""

    values = product([0, 1], repeat=3)
    uniques = sorted(["".join(map(str, x)) for x in values], key=lambda x: int(x, 2))
    zeroes = {}
    ones = {}
    for st in uniques:
        zero = len(re.findall(f"(?={st}0)", strng))
        one = len(re.findall(f"(?={st}1)", strng))
        zeroes[st] = zero
        ones[st] = one
    return zeroes, ones


def make_prediction(strng):
    """Function used to predict a binary string according to
    the frequency of 0's and 1's.
    Returns the predicted string and the count of correct predicted characters"""

    zeroes, ones = analyze(strng)
    predicted = f"{''.join([str(random.randint(0, 1)) for _ in range(3)])}"
    for i in range(len(strng) -  3):
        triad = strng[i] + strng[i + 1] + strng[i + 2]
        if zeroes[triad] > ones[triad]:
            predicted += "0"
        elif zeroes[triad] < ones[triad]:
            predicted += '1'
        else:
            predicted += str(random.randint(0, 1))
    correct_predicted = 0
    for i in range(3, len(strng)):
        if strng[i] == predicted[i]:
            correct_predicted += 1
    return predicted, correct_predicted


def main():
    """Main function of the game. Updates the user's budget according to how many
    character were guessed by computer and prints out the predicted string"""

    analyze(random_string())
    budget = 1000
    print("""You have $1000. Every time the system successfully predicts your next press, you lose $1.
Otherwise, you earn $1. Print 'enough' to leave the game. Let's go!""")
    while True:
        message = input("\nPrint a random string containing 0 or 1:\n")
        if message == "enough":
            print("Game over!")
            break
        else:
            to_predict = clean_string(message)
            if len(to_predict) > 3:
                predicted, correct_predicted = make_prediction(to_predict)
                percent = round(correct_predicted / (len(to_predict) - 3) * 100, 2)
                diff = len(to_predict) - 3 - correct_predicted
                budget -= correct_predicted
                budget += diff
                print(f"prediction:\n{predicted}\n")
                print(f"Computer guessed right {correct_predicted} out of {len(to_predict) - 3} symbols ({percent} %)")
                print(f"Your capital is now ${budget}\n")

if __name__ == "__main__":
    main()