import requests
import os
import sys
from collections import deque
from bs4 import BeautifulSoup
from colorama import init, Fore
from termcolor import colored
init()

class Browser:

    def __init__(self):
        self.url = None
        self.stack = deque()

    def make_dir(self):
        drr = sys.argv[1]
        if not os.path.exists(drr):
            dr = os.mkdir(drr)

        return os.path.abspath(drr)

    def create_file(self, path):
        abs_path = f"{self.make_dir()}\\{path}"
        if not os.path.isfile(abs_path):
            r = requests.get(self.url)
            r.encoding = "utf-8"
            soup = BeautifulSoup(r.content, "html.parser")
            content = soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6", "a", "ul", "ol", "li"])
            with open(abs_path, "w+") as file:
                for c in content:
                    if c.name == "a":
                        c = c.text.strip().replace("\n", "")
                        file.write(Fore.BLUE + colored(c) + "\n")
                    else:
                        c = c.text.strip().replace("\n", "")
                        file.write(Fore.WHITE + c + "\n")
                file.seek(0)
                txt = file.read()
                print(txt, "\n")
                return (txt)
        else:
            with open(abs_path, "r") as file:
                txt = file.read()
                print(txt, "\n")
                return (txt)


    def back(self):

        try:
            print(self.stack.pop(), "\n")
        except IndexError:
            print()


    def menu(self):
        self.make_dir()
        while True:
            self.url = input()
            if self.url == "exit":
                break
            else:
                if "." not in self.url  and self.url != "back":
                    print("Error: Incorrect URL")
                else:
                    if self.url != "back":
                        if self.url.startswith("https://"):
                            filename = self.url.strip("https://").split(".")
                            filename.pop()
                            try:
                                r = requests.get(self.url)
                                self.stack.appendleft(self.create_file(".".join(filename)))
                            except requests.exceptions.ConnectionError:
                                print("Error: Incorrect URL\n")
                                continue

                        elif not self.url.startswith("https://"):
                            self.url = "https://" + self.url
                            filename = self.url.strip("https://").split(".")
                            filename.pop()
                            try:
                                r = requests.get(self.url)
                                self.stack.appendleft(self.create_file(".".join(filename)))
                            except requests.exceptions.ConnectionError:
                                print("Error: Incorrect URL\n")
                                continue

                        else:
                            print("Error : Incorrect URL")
                    else:
                        self.back()
browser = Browser()

browser.menu()
