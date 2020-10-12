"""Rock Paper Scisssors game using OOP"""

import random
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove

class RockPaperScissors:
    """initializing the 'global' atributtes"""
    def __init__(self):
        self.defeat = {"scissors": "rock", "paper" : "scissors", "rock" : "paper"}
        self.choices = ["rock", "paper", "scissors"]
        self.score = 0
        self.name = input("Enter your name: ")



    def file(self):
        """method keeping track of players rating in 'rating.txt' file"""

        file = open("rating.txt", "r+", encoding="utf-8")
        for line in file:
            line1 = line.rstrip()
            if self.name == line1.split()[0]:
                score = line1.split()[1]
                self.score = int(score)

                self.play()
                print(line.replace(score, str(self.score)), file=file, flush=True)
                file.close()
                break
            else:
                if self.name != line1.split()[0]:
                    continue
                else:
                    score = line1.split()[1]
                    self.play()
                    print(line.replace(score, str(self.score)), file=file, flush=True)
                    file.close()
                    break
        else:
            self.play()
            print(self.name, self.score, sep=" ", file=file, flush=True)
            file.close()







    def play(self):
        """method is checking word imputed by user against the initial dict of words,
         and increase rating if user wins,or is a draw"""

        print(f"Hello, {self.name}")
        self.rewrite_options()
        print("Okay, let's start")
        while True:

            user_input = input("Enter your choice: ")
            if user_input == "!rating":
                print(f"Your rating: {self.score}")
                continue
            elif user_input == "!exit":
                print("Bye!")
                break
            else:
                choice = random.choice(self.choices)
                if user_input not in self.choices:
                    print("Invalid input")
                elif user_input == choice:
                    self.score += 50
                    print(f"There is a draw ({choice})")
                elif user_input in self.defeat[choice]:
                    self.score += 100
                    print(f"Well done. The computer chose {choice} and failed")
                else:
                    print(f"Sorry, but the computer chose {choice}")


    def rewrite_file(self):
        """method updating rating of all players by rewriting 'rating.txt' file"""

        names = []
        dict_ = {}
        fake_f = "rating.txt"
        abs_path = "C:/Users/dandei/Desktop/jetBrain_projects/rock_paper_scissors/rating.txt"  #change this with your path
        fake_f, abs_path = mkstemp()
        with fdopen(fake_f, "w") as new_file:
            with open("rating.txt", "r+", encoding="utf-8") as file:
                content = file.read()
                content = content.split("\n")
                for element in content:
                    if len(element) > 1:
                        element = element.split()
                        names.append(element)
                dict_ = dict(names)
                for key, value in dict_.items():
                    print(key, value, sep=" ", file=new_file)
        copymode("rating.txt", abs_path)
        remove("rating.txt")
        move(abs_path, "rating.txt")

    def rewrite_options(self):
        """method let's user choose between playing the classic game or
        palying the game with more options. Changes the initial dict of words as user
        inputs more options"""

        choice = input("Enter your game options: ")
        choices = choice.split(",")
        defeat_by = {}
        new_list = []
        if choice == "":
           return None
        else:
            self.choices = choices
            for i in range(len(choices)):
                new_list = choices[i + 1:] + choices[:i]

                #wins_over
                defeat_by[choices[i]] = new_list[:(len(new_list)) // 2]

            self.defeat = defeat_by







#If rating.txt does not exist, it get's created here
fill = open("rating.txt", "a", encoding="utf-8")
fill.close()
#creating instance of the RockPaperScissors class
rps = RockPaperScissors()
rps.file()
rps.rewrite_file()
