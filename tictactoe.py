"""Script for TicTacToe game"""
import random
import sys


class TicTacToe:
    """Initialising game class"""

    def __init__(self):

        self.field = ["___", "___", "___"]
        self.comm = None

    def __str__(self):
        """returns game board i a nice formated way"""
        line1 = " ".join(self.field[2]).replace("_", " ")
        line2 = " ".join(self.field[1]).replace("_", " ")
        line3 = " ".join(self.field[0]).replace("_", " ")

        return f"\n{'-' * 9}\n| {line1} |\n| {line2} |\n| {line3} |\n{'-' * 9}"


    def comp_move(self):
        """it makes a random move within available spaces"""
        possible_moves = [[i, j] for i, _ in enumerate(self.field)
                          for j, let in enumerate(self.field[i])
                          if let == "_"]

        move = random.choice(possible_moves)
        row = move[0]
        coll = move[1]
        return coll, row

    def medium_move(self):
        """it check's to see if it can win or block opponent within a single move
        else pick a random corner or edge else center"""
        coll = 0
        row = 0
        move  = [row, coll]
        possible_moves = [[i, j] for i, _ in enumerate(self.field)
                          for j, let in enumerate(self.field[i])
                          if let == "_"]
        for let in ["X" if "X" else "O"]:
            for move in possible_moves:
                field_copy = self.field[:]
                field_copy = [" ".join(line).split() for line in field_copy]
                row = move[0]
                coll = move[1]
                field_copy[row][coll] = let
                if self.is_winner(field_copy, let):
                    return coll, row



        corners = [[0, 0], [0, 2], [2, 0], [2, 2]]
        corners_move = []
        for i in possible_moves:
            if i in corners:
                corners_move.append(i)
        if len(corners_move) > 0:
            move = random.choice(corners_move)
            row = move[0]
            coll = move[1]
            return coll, row

        if [1, 1] in possible_moves:
            coll = 1
            row = 1
            return coll, row

        edges = [[0, 1], [1, 0], [1, 2], [2, 1]]
        edges_move = []
        for i in possible_moves:
            if i in edges:
                edges_move.append(i)
        if len(edges_move) > 0:
            move = random.choice(edges_move)
            row = move[0]
            coll = move[1]
        return coll, row

        #hard play section

    def coord(self, field):
        """returns coord for hard level"""
        (m, coll, row) = self.max_alpha_beta(field, -2, 2)
        coord = [coll, row]
        return coord

    def max_alpha_beta(self, field, alpha, beta):
        """alpha beta pruning(not the optim approach; some spaghetti code in here)"""
        x, o = self.first_move()
        max_val = -2
        p_row = None
        p_coll = None
        if x == o:
            if self.is_winner(field, "X") == True:
                return(1, 0, 0)
            elif self.is_winner(field, "O") == True:
                return(-1, 0, 0)
            elif self.draw(field) == True:
                return(0, 0, 0)
        elif o < x:
            if self.is_winner(field, "X") == True:
                return(-1, 0, 0)
            elif self.is_winner(field, "O") == True:
                return(1, 0, 0)
            elif self.draw(field) == True:
                return(0, 0, 0)

        for row in range(len(field)):
            for col in range(len(field[0])):
                if field[row][col] == "_":
                    for let in ["O", "X"]:
                        field[row][col] = let
                        (m, min_coll, min_row) = self.min_alpha_beta(field, alpha, beta)
                        if m > max_val:
                            max_val = m
                            p_coll = col
                            p_row = row
                        field[row][col] = "_"

                        if max_val >= beta:
                            return(max_val, p_coll, p_row)
                        if max_val > alpha:
                            alpha = max_val

        return(max_val, p_coll, p_row)

    def min_alpha_beta(self,field, alpha, beta):
        """alpha beta pruning(not the optim approach; some spaghetti code in here)"""
        x, o = self.first_move()
        min_val = 2
        q_row = None
        q_coll = None
        if x == o:
            if self.is_winner(field, "X") == True:
                return(-1, 0, 0)
            elif self.is_winner(field, "O") == True:
                return(1, 0, 0)
            elif self.draw(field) == True:
                return(0, 0, 0)
        elif o < x:
            if self.is_winner(field, "X") == True:
                return(1, 0, 0)
            elif self.is_winner(field, "O") == True:
                return(-1, 0, 0)
            elif self.draw(field) == True:
                return(0, 0, 0)

        for row in range(len(field)):
            for col in range(len(field[0])):
                for let in ["X", "O"]:
                    if field[row][col] == "_":
                        field[row][col] = let
                        (m, max_row, max_coll) = self.max_alpha_beta(field, alpha, beta)
                        if m < min_val:
                            min_val = m
                            q_coll = col
                            q_row = row
                        field[row][col] = "_"

                        if min_val <= alpha:
                            return(min_val, q_coll, q_row)
                        if min_val < beta:
                            beta = min_val

        return(min_val, q_coll, q_row)


    def first_move(self):
        """count X's and O's in the field"""
        count_x = self.field[0].count("X") + self.field[1].count("X") + self.field[2].count("X")
        count_o = self.field[0].count("O") + self.field[1].count("O") + self.field[2].count("O")

        return count_x, count_o


    def move(self, player, let):
        """make's a move on the board depending on witch level player we choose"""
        field = [" ".join(line).split() for line in self.field]
        try:
            if player == "easy":
                coll, row = self.comp_move()
                print(f'Making move level "{player}"')
                field[row][coll] = let
                self.field = field
                return self.field
            elif player == "medium":
                coll, row = self.medium_move()
                print(f'Making move level "{player}"')
                field[row][coll] = let
                self.field = field
                return self.field
            elif player == "hard":
                coll, row = self.coord(field)
                print(f'Making move level "{player}"')
                field[row][coll] = let
                self.field = field
                return self.field
            elif player == "user":
                coll, row = input("Enter coordinates: ").split()
                if int(row) > 3 or int(coll) > 3 or int(row) < 1 or int(coll) < 1:
                    print("Coordinates should be from 1 to 3!")
                elif str(row).isalpha() or str(coll).isalpha():
                    print("You should enter numbers!")
                elif field[int(row) - 1][int(coll) - 1] != "_":
                    print("This cell is occupied! Choose another one!")
                else:
                    field[int(row) - 1][int(coll) - 1] = let
                    self.field = field
                    return self.field

        except ValueError:
            print("You should enter numbers!")

    def handle_input(self):
        """returns the imput if imput is correct else raises a message"""
        comm = input("Input command: ")
        if comm == "exit":
            sys.exit()
        elif len(comm.split()) != 3:
            return "Bad parameters!"
        elif (not comm.startswith("start") and
              ("easy" not in comm.split() or "user"
               not in comm.split() or "medium" not in comm.split())):
            return "Bad parameters!"
        else:
            self.comm =  comm
            return self.comm


    def is_winner(self, field, let):
        """Function check's for a winner"""
        line1 = "".join(field[0])
        line2 = "".join(field[1])
        line3 = "".join(field[2])
        return (line1.count(let) == 3 or line2.count(let) == 3 or line3.count(let) == 3) or\
            (line1[0] == line2[0] == line3[0] == let) or (line1[1] == line2[1] == line3[1] == let) or\
            (line1[2] == line2[2] == line3[2] == let) or (line1[0] == line2[1] == line3[2] == let) or\
            (line1[2] == line2[1] == line3[0] == let)

    def draw(self, field):
        """Function check's if is a draw"""
        line1 = " ".join(field[0])
        line2 = " ".join(field[1])
        line3 = " ".join(field[2])
        return ("_" not in line1 and "_" not in line2 and "_" not in line3) and\
             not self.is_winner(self.field, "X") and not self.is_winner(self.field, "O")

    def fight(self):
        """Function check's if there is a winner,
        or a draw else populates the field with X and O"""
        command = ""

        while True:
            self.field = ["___", "___", "___"]
            if self.handle_input() != "Bad parameters!":
                while True:
                    x, o = self.first_move()
                    print(f"{self.__str__()}")
                    if self.draw(self.field):
                        print("Draw\n")
                        break
                    elif self.is_winner(self.field, "X"):
                        print("X wins\n")
                        break
                    elif self.is_winner(self.field, "O"):
                        print("O wins\n")
                        break
                    else:
                        if x == o:
                            self.move(self.comm.split()[1], "X")
                        elif o < x:
                            if self.is_winner(self.field, "X") == False or self.draw(self.field) == False:
                                self.move(self.comm.split()[-1], "O")
            else:
                print("Bad parameters!")


my_game = TicTacToe()
my_game.fight()
