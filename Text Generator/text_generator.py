from random import choice, choices
from nltk.tokenize import WhitespaceTokenizer
from collections import defaultdict, Counter

"""This project uses some basic nltk features as well as other libraries to
generate preudo sentences using the idea of markow chains."""


class TextGenerator:

    def __init__(self):
        self.path = input()
        self.tokens = self.tokens()
        self.ngrams = self.ngrams()

    def read_file(self):
        """method is used to read the corpus file that will be used
        to generate the sentences"""

        with open(self.path, encoding="utf-8") as file:
            text = file.read()
        return text

    def tokens(self):
        """method is used to parse the text file and to return
        a list of all tokens"""
        text = self.read_file()
        tk = WhitespaceTokenizer()
        return tk.tokenize(text)

    def ngrams(self):
        """method returns a dict using every 2 words as key and the value is a counter dict of every word
         that is a possible folower of the first 2 words(like nltk.FreqDist)"""
        ngrams = defaultdict(Counter)
        for i in range(len(self.tokens) - 2):
            ngrams[" ".join(self.tokens[i:i + 2])].update((self.tokens[i + 2],))
        return ngrams

    def find_start(self):
        """method is used to find the first words of the sentence"""
        starts = [pair for pair in list(self.ngrams) if pair.split()[0][0].isupper() and pair.split()[0][-1] not in "!?."]
        return choice(starts).split()

    def make_sentence(self, n=5):
        """main method of the script. It randomly chooses the next words in
        sentence accordingly to their weight in the original text and returns the new sentence"""
        result = []
        while True:
            if len(result) == 0:
                result = self.find_start()
            w1 = " ".join(result[-2:])
            w2 = choices(list(self.ngrams[w1].keys()), list(self.ngrams[w1].values()))
            result.append(*w2)

            if w2[0][-1] in ".!?":
                if len(result) < n:
                    result = []
                    continue
                return " ".join(result)


if __name__ == "__main__":
    text_gen = TextGenerator()
    for _ in range(10):
        print(text_gen.make_sentence())
