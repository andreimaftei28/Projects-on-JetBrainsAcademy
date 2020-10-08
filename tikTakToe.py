"""Script for TicTacToe game"""
class TicTacToe:
    field = []
    def __init__(self, moves):
        self.moves = moves
        for i in range(0, len(self.moves), 3):
            self.field.append(moves[i : i + 3])
    def __str__(self):

        line1 = " ".join(self.field[0]).replace("_", " ")
        line2 = " ".join(self.field[1]).replace("_", " ")
        line3 = " ".join(self.field[2]).replace("_", " ")

        return f"\n{'-' * 9}\n| {line1} |\n| {line2} |\n| {line3} |\n{'-' * 9}"
    def x_wins(self):
        """Function check's if X is winner"""
        line1 = "".join(self.field[0])
        line2 = "".join(self.field[1])
        line3 = "".join(self.field[2])

        if "XXX" in line1 or "XXX" in line2 or "XXX" in line3:
            return f"{self.__str__()}\nX wins"
        elif line1[0] == "X" and line2[0] == "X" and line3[0] == "X":
            return f"{self.__str__()}\nX wins"
        elif line1[1] == "X" and line2[1] == "X" and line3[1] == "X":
            return f"{self.__str__()}\nX wins"
        elif line1[2] == "X" and line2[2] == "X" and line3[2] == "X":
            return f"{self.__str__()}\nX wins"
        elif line1[0] == "X" and line2[1] == "X" and line3[2] == "X":
            return f"{self.__str__()}\nX wins"
        elif line1[2] == "X" and line2[1] == "X" and line3[0] == "X":
            return f"{self.__str__()}\nX wins"
        else:
            return 0



    def o_wins(self):
        """Function check's if O is winner"""
        line1 = "".join(self.field[0])
        line2 = "".join(self.field[1])
        line3 = "".join(self.field[2])
        #print(line1, line2, line3)


        if "OOO" in line1 or "OOO" in line2 or "OOO" in line3:
            return f"{self.__str__()}\nO wins"
        elif line1[0] == "O" and line2[0] == "O" and line3[0] == "O":
            return f"{self.__str__()}\nO wins"
        elif line1[1] == "O" and line2[1] == "O" and line3[1] == "O":
            return f"{self.__str__()}\nO wins"
        elif line1[2] == "O" and line2[2] == "O" and line3[2] == "O":
            return f"{self.__str__()}\nO wins"
        elif line1[0] == "O" and line2[1] == "O" and line3[2] == "O":
            return f"{self.__str__()}\nO wins"
        elif line1[2] == "O" and line2[1] == "O" and line3[0] == "O":
            return f"{self.__str__()}\nO wins"
        else:
            return 0



    def draw(self):
        """Function check's if is a draw"""
        line1 = " ".join(self.field[0])
        line2 = " ".join(self.field[1])
        line3 = " ".join(self.field[2])

        if ("_" not in line1 and "_" not in line2 and "_" not in line3) and (self.x_wins() == 0 or self.o_wins() == 0):
            #print(line1, line2, line3)
            return f"{self.__str__()}\nDraw"
        return 0

    def impossible(self):
        """Function check's for a impossible situation"""
        count_x = self.moves.count("X")
        count_o = self.moves.count("O")
        if abs(count_x - count_o) >= 2:
            return f"{TicTacToe.__str__(self)}\nImpossible"
        elif self.x_wins() and self.o_wins():
            return f"{TicTacToe.__str__(self)}\nImpossible"
        else:
            return 0


    def fight(self):
        """Function check's if there is a winner,
        an impossible situation or a draw else populates the field with X and O"""

        field = self.field
        line1 = " ".join(field[0])
        line2 = " ".join(field[1])
        line3 = " ".join(field[2])
        field1 = [line3.split(), line2.split(), line1.split()]
        while True:

            if self.x_wins() != 0:
                return self.x_wins()
            elif self.o_wins() != 0:
                return self.o_wins()
            elif self.draw() != 0:
                return self.draw()
            elif self.impossible() != 0:
                return self.impossible()
            else:
                print(f"{self.__str__()}\n")
                try:
                    coll, row = input("Enter coordinates: ").split()
                    if int(row) > 3 or int(coll) > 3:
                        print("Coordinates should be from 1 to 3!")
                    elif row.isalpha() or coll.isalpha():
                        print("You should enter numbers!")
                    elif field1[int(row) - 1][int(coll) - 1] != "_":
                        print("This cell is occupied! Choose another one!")
                    else:
                        field1[int(row) - 1][int(coll) - 1] = "X"
                        field = [field1[2], field1[1], field1[0]]
                        self.field = field
                except ValueError:
                    print("You should enter numbers!")

            if self.x_wins() != 0:
                return self.x_wins()
            elif self.o_wins() != 0:
                return self.o_wins()
            elif self.draw() != 0:
                return self.draw()
            elif self.impossible():
                return self.impossible()
            else:
                print(f"{self.__str__()}\n")
                try:
                    coll, row = input("Enter coordinates: ").split()
                    if int(row) > 3 or int(coll) > 3:
                        print("Coordinates should be from 1 to 3!")
                    elif row.isalpha() or coll.isalpha():
                        print("You should enter numbers!")
                    elif field1[int(row) - 1][int(coll) - 1] != "_":
                        print("This cell is occupied! Choose another one!")
                    else:
                        field1[int(row) - 1][int(coll) - 1] = "O"
                        field = [field1[2], field1[1], field1[0]]
                        self.field = field


                except ValueError:
                    print("You should enter numbers!")



my_game = (TicTacToe("_________"))
print(my_game.fight())
