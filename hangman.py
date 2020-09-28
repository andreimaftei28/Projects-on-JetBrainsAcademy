import random

print('H A N G M A N \n')

words = ['python', 'java', 'kotlin', 'javascript']
start_message ='Type "play" to play the game, "exit" to quit: '
message = "Input a letter: "


while True:
    n = 8
    word1 = list(random.choice(words))
    dashes = ("-" * len(word1))
    temp = list(dashes)
    temp2 = []
    mess = input(start_message)
    if mess == "exit":
        break
    elif mess == "play":
        while n > 0 and temp != word1:
            print()
            print(dashes)
            letter = input(message)
            if letter in word1:
                if letter not in temp:
                    for i, let in enumerate(word1):
                        if let == letter:
                            temp[i] = letter
                            dashes = "".join(temp)
                            if temp == word1:
                                print()
                                print(dashes)
                                print("You guessed the word!")
                                print("You survived!")
                                break
                else:
                    print("You already typed this letter")
            elif letter.isupper() or not letter.isalpha():
                if len(letter) > 1:
                    print("You should input a single letter")
                else:
                    print("It is not an ASCII lowercase letter")
            elif len(letter) > 1 or len(letter) == 0:
                print("You should input a single letter")
            else :
                if letter in temp2:
                    print("You already typed this letter")
                else:
                    temp2.append(letter)
                    print("No such letter in the word")
                    n -= 1

            if n == 0:
                print("You are hanged!")
                break
    else:
        continue
