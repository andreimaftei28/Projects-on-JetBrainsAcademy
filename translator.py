"""Program can be used to translate in different languages online using requests"""

import requests
from bs4 import BeautifulSoup
import sys

class Translator():


    def __init__(self):
        self.word = None
        self.first_choice = None
        self.second_choice= None
        self.list_lang = [ "arabic", "german", "english", "spanish", "french",
                          "hebrew", "japanese", "dutch", "polish", "portuguese",
                          "romanian", "russian", "turkish"]

        self.status = ""

    def create_req(self):
        """method is creating request parsing response from server and writing
        human readeble response to a file"""


        full_lang = self.second_choice.title()
        headers = {"User-Agent": "Mozilla/5.0"}
        url = f"https://context.reverso.net/translation/{self.first_choice}-{self.second_choice}/{self.word}"
        s = requests.Session()
        req = s.get(url, headers=headers)
        req.encoding = "utf-8"
        if req:
            self.status = f"{req.status_code} Ok"
        else:
            self.status = req.status_code
            if self.status == 404:
                print(f"Sorry, unable to find {self.word}")
                sys.exit()
            elif self.status == 408:
                print("Something wrong with your internet connection")
                sys.exit()
        soup = BeautifulSoup(req.content, "html.parser")
        w_to_find = soup.find('div', {'id': 'translations-content'})
        section = soup.find("section", {"id": "examples-content"})
        words = [word for word in w_to_find.text.split()]
        phrase = [elem.text.strip() for elem in section.find_all("span", {"class": "text"})]
        print(f"{full_lang} Translations:")
        print(words[0])
        print(f"\n{full_lang} Examples:")
        print(phrase[0] + ":\n" + phrase[1])
        with open(f"{self.word}.txt", "a+", encoding="utf-8") as file:
            print(f"{full_lang} Translations:", file=file, flush=True, end="\n")
            print(words[0], file=file, flush=True, end="\n")
            print(f"\n{full_lang} Examples:", file=file, flush=True, end="\n")
            print(phrase[0] + ":\n" + phrase[1], file=file, flush=True, end= "\n")
            #file.seek(0)
            #print(file.read())

    def translate(self):
        """method used to handle arguments from terminal """
        args = sys.argv
        self.first_choice = args[1]
        self.second_choice = args[2]
        self.word = args[3]

        return  self.first_choice, self.second_choice, self.word


    def multiple_trans(self):
        """method is used to detemine single language translation or multiple"""

        self.translate()
        if self.second_choice != "all":
            if self.second_choice not in self.list_lang:
                print(f"Sorry, the program doesn't support {self.second_choice}")
            else:
                print(self.status)
                self.create_req()
        else:
            languages = [x for x in self.list_lang if x != self.first_choice]
            self.second_choice = languages[0]
            print(self.status)
            for i in range(len(languages)):
                self.second_choice = languages[i]
                self.create_req()

trans = Translator()
if __name__ == "__main__":

    trans.multiple_trans()

