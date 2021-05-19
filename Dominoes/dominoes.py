"""Script to simulate Dominoes game"""

import random
from collections import deque


class Domino:

    def __init__(self):
        self.stock = []
        self.computer = []
        self.player = []
        self.domino_snake = deque()

    def distribution(self):
        """method used to establish the initial distribution of pieces"""
        pieces = list()
        next_player = None

        # initial pieces distribution
        for i in range(7):
            for j in range(i, 7):
                pieces.append([i, j])
        random.shuffle(pieces)

        self.stock = pieces[:14]
        self.computer = pieces[14:21]
        self.player = pieces[21:]
        del pieces

        # choose the next player
        for i in range(6, -1, -1):
            if [i, i] in self.computer:
                self.computer.remove([i, i])
                self.domino_snake.append(str([i, i]))
                next_player = 'player'
                break
            elif [i, i] in self.player:
                self.player.remove([i, i])
                self.domino_snake.append(str([i, i]))
                next_player = 'computer'
                break

        return next_player

    def snake_display(self):
        """method used to print the 'domino snake' in a nice formatted way"""

        snake = list(self.domino_snake)
        if len(snake) <= 6:
            print("".join(snake))
        else:
            print("".join(snake[:3]), "...", "".join(snake[-3:]), sep="")

    def play(self, pieces, position):
        """method for checking where the current piece will be appended on the domino stack"""

        if position < 0:
            piece = pieces.pop(abs(position) - 1)
            if int(self.domino_snake[0][1]) == piece[0]:
                piece.reverse()
            self.domino_snake.appendleft(str(piece))
        elif position > 0:
            piece = pieces.pop(abs(position) - 1)
            if int(self.domino_snake[-1][-2]) == piece[1]:
                piece.reverse()
            self.domino_snake.append(str(piece))
        elif position == 0:
            if len(self.stock):
                pieces.append(self.stock.pop(0))

    def legal_move(self, pieces, position):
        """method for checking if a move is legal according to the game rules"""
        snake_queue = None
        piece = pieces[abs(position) - 1]
        if position > 0:
            snake_queue = int(self.domino_snake[-1][-2])
        elif position < 0:
            snake_queue = int(self.domino_snake[0][1])

        if snake_queue in piece or position == 0:
            return True
        else:
            return False

    def intelligent_computer(self):

        count = []
        for i in range(7):
            nb_snake = "".join(self.domino_snake).count(str(i))
            nb_computer = sum([j.count(i) for j in self.computer])
            count.append(nb_snake + nb_computer)

        scores = {}
        for i, piece in enumerate(self.computer):
            scores[i+1] = count[piece[0]] + count[piece[1]]

        scores = sorted(scores.items(), key=lambda x: x[1])
        scores.reverse()

        return scores

    def check_end_game(self):
        """method for checking end of the game"""

        first_piece = self.domino_snake[0][1]
        last_piece = self.domino_snake[-1][-2]
        end = True
        if len(self.player) == 0:
            print("Status: The game is over. You won!")
        elif len(self.computer) == 0:
            print("Status: The game is over. The computer won!")
        elif first_piece == last_piece and str(self.domino_snake).count(first_piece) >= 8:
            print("Status: The game is over. It's a draw!")
        else:
            end = False

        return end

    def game(self):
        """main method"""
        next_player = self.distribution()
        if next_player:
            while True:
                print(70 * "=")
                print(f"Stock size: {len(self.stock)}")
                print(f"Computer pieces: {len(self.computer)}")
                print()
                self.snake_display()
                print()
                print("Your pieces:")
                [print(i + 1, ":", j, sep="") for i, j in enumerate(self.player)]
                print()
                print("Computer", self.computer, sep='\n')
                if self.check_end_game():
                    break

                if next_player == 'player':
                    print("Status: It's your turn to make a move. Enter your command.")
                    while True:
                        try:
                            user_choice = int(input())
                        except ValueError:
                            print("Invalid input. Please try again.")
                            continue

                        if abs(user_choice) <= len(self.player):
                            if not self.legal_move(self.player, user_choice):
                                print("Illegal move. Please try again.")
                                continue
                            else:
                                self.play(self.player, user_choice)
                                next_player = 'computer'
                                break
                        else:
                            print("Invalid input. Please try again.")
                            continue
                elif next_player == 'computer':
                    print("Status: Computer is about to make a move. Press Enter to continue...")
                    input()

                    position = 0
                    for position_piece in [i[0] for i in self.intelligent_computer()]:
                        if self.legal_move(self.computer, position_piece):
                            position = position_piece
                            break
                        elif self.legal_move(self.computer, -position_piece):
                            position = -position_piece
                            break

                    self.play(self.computer, position)
                    next_player = 'player'


domino_party = Domino()
domino_party.game()