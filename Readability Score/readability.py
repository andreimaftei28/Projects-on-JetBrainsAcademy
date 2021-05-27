import re
import argparse
import math


parser = argparse.ArgumentParser()
parser.add_argument("--infile")
parser.add_argument("--words")
args = parser.parse_args()


def readability(score):
    """
        Creates a dict with readability scores in from 1 to 14 as keys and
        ages from 5 to 25 as values
        Returns the age corresponding to a specific score
        Used to return the age corresponding to ARI, FK, SMOG, CL
    """

    score = math.ceil(score)
    indexes = range(1, 15)
    ages = [6, 7]
    ages.extend([x for x in range(9, 19)])
    ages.extend([24, 25])
    scores = dict(zip(indexes, ages))
    return scores[score] if score <= 14 else scores[14]


def prob_readability(score):
    """
        Creates a dict with readability scores in from 5 to 10 as keys and
        ages from 10 to 24 as values
        Returns the age corresponding to a specific score
        Used to return the age corresponding to PB
    """

    score = math.ceil(score)
    indexes = [i for i in range(5, 11)]
    ages = [i for i in range(10, 19, 2)]
    ages.append(24)
    scores = dict(zip(indexes, ages))
    return scores[score] if score <= 10 else scores[10]


def read_file(file):
    """returns text from input file"""

    with open(file, "r") as f:
        text = f.read()
    return text


def preprocess_text(text):
    """
        Cleans the punctuation marks from text
        Returns a list with all the words from text
    """
    pattern = r"[\.,\?\!:\(\); ]"
    text = text.lower().strip()
    word_ = re.split(pattern, text)
    word_list = [x for x in word_ if x not in "?!().,:; "]
    return word_list


def syllable_count(word):
    """Calculates and returns the number of syllables in a given word"""

    count = 0
    vowels = "aeiouy"
    if word[-1] in ".,?!":
        word = word[:-1]
    word = word.lower()
    if word[0] in vowels:
        count += 1
    for i in range(1, len(word)):
        if word[i] in vowels and word[i - 1] not in vowels:
            count += 1
    if word.endswith("e"):
        count -= 1
    if count == 0:
        count += 1
    return count


def text_props(text):
    """
        Returns a tupple containing number of characters,
        words, difficult words, sentences, syllables, words with more then 2 syllable
        in a given text
    """

    pattern = r"([\.\?\!])"
    corpus = read_file(args.words).strip().split()
    chars_count = (len("".join(text.split())))
    words_count = (len(text.split()))
    sentences_list = re.split(pattern, text)
    sentences = [sentence for sentence in sentences_list if sentence not in "?!." and len(sentence) > 0]
    syllables = [syllable_count(word) for word in preprocess_text(text)]
    syllables_count = sum(syllables)
    polysyllables_count = len([syllable for syllable in syllables if syllable > 2])
    difficult_words = [x for x in preprocess_text(text) if x not in corpus]
    difficult_words_count = len(difficult_words)
    return chars_count, words_count, len(sentences), syllables_count, polysyllables_count, difficult_words_count


def calculate_ari(text):
    """
        It produces an approximate representation of the grade level
        needed to comprehend the text - Automated Readability Index.
    """

    chars_count, words_count, sentences_count, *other = text_props(text)
    score = 4.71 * (chars_count / words_count) + (0.5 * words_count / sentences_count) - 21.43
    return round(score, 2)


def calculate_f_k(text):
    """
        It is more or less the number of years of
        education generally required to understand a text.
    """

    chars_count, words_count, sentences_count, syllables_count, *others = text_props(text)
    score = 0.39 * words_count / sentences_count + (11.8 * syllables_count / words_count) - 15.59
    return round(score, 2)


def calculate_smog(text):
    """
        Simple Measure of Gobbledygook (SMOG) is a simplification of Gunning Fog,
        also estimating the years of formal education needed to understand a text
    """

    *other, sentences_count, syllables_count, polysyllables_count, difficult_words = text_props(text)
    score = 1.043 * math.sqrt((polysyllables_count * 30) / sentences_count) + 3.1291
    return round(score, 2)


def calculate_c_l(text):
    """
        It approximates the grade level thought necessary to comprehend a given text.
    """

    chars_count, words_count, sentences_count, *other = text_props(text)
    score = (5.88 * chars_count / words_count) - (29.6 * (sentences_count / words_count)) - 15.8
    return round(score, 2)


def calculate_p_b(*args):
    """
        Determines how difficult a text is according to the number of words that are, most likely, unknown to readers.
        The other formulas we referred to based the score on the number of words and sentences only
    """
    words_count, sentences_count, diff_words_count = args[0][1], args[0][2], args[0][-1]
    dif_percent = diff_words_count / words_count * 100
    score = 0.1579 * dif_percent + (0.0496 * words_count / sentences_count)
    if dif_percent >= 5:
        score += 3.6365
        return round(score, 2)
    return round(score, 2)


def main():
    """
        Core function of this script. Calls all other function to print
        all the results in a nice formatted way.
    """

    text = read_file(args.infile)
    chars_count, words_count, sentences_count, syllables_count, polysyllables_count, difficult_words = text_props(text)
    ari = calculate_ari(text)
    fk = calculate_f_k(text)
    smog = calculate_smog(text)
    cl = calculate_c_l(text)
    pb = calculate_p_b(text_props(text))
    avg_age = (readability(ari) + readability(fk) + readability(smog) + readability(cl) + prob_readability(pb)) / 5

    keys = range(1, 7)
    outputs = [f"Automated Readability Index: {ari} (about {readability(ari)}-years-olds).",
               f"Flesch–Kincaid readability tests: {fk} (about {readability(fk)}-years-olds).",
               f"Simple Measure of Gobbledygook: {smog} (about {readability(smog)}-years-olds).",
               f"Coleman–Liau index: {cl} (about {readability(cl)}-years-olds).",
               f"Probability-based score: {pb} ({prob_readability(pb)}-years-olds)",
               f"\nThis text should be understood in average by {avg_age}-years-olds"]
    outputs_dict = dict(zip(keys, outputs))
    print(f"The text is:\n{text}\n")
    print(f"Words: {words_count}\nDifficult words: {difficult_words}\nSentences: {sentences_count}\nCharacters: {chars_count}\nSyllables: {syllables_count}\nPolysyllables: {polysyllables_count}")
    option = input("Enter the score you want to calculate (ARI, FK, SMOG, CL, PB, all): ")
    print()
    if option == "ARI":
        print(outputs_dict[1])
    elif option == "FK":
        print(outputs_dict[2])
    elif option == "SMOG":
        print(outputs_dict[3])
    elif option == "CL":
        print(outputs_dict[4])
    elif option == "PB":
        print(outputs_dict[5])
    else:
        for i in range(1, 6):
            print(outputs_dict[i])
        print(outputs_dict[6])


if __name__ == '__main__':
    main()