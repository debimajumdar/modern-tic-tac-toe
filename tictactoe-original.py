tictac.py
# Assignment: Programming Assignment 2
# Author: Debi Majumdar
# Date: 2/5/23
# File: tictac.py is a Python program that implements a tic-tac-toe game
# Input: user responses (strings)
# Output: interactive text messages and a tic-tac-toe board

from board import Board
from player import Player

# main program
print("Welcome to TIC-TAC-TOE Game!")
while True:
    board = Board()
    player1 = Player("Bob", "X")
    player2 = Player("Alice", "O")
    turn = True
    while True:
        board.show()
        if turn:
            player1.choose(board)
            turn = False
        else:
            player2.choose(board)
            turn = True
        if board.isdone():
            break
    board.show()
    if board.get_winner() == player1.get_sign():
        print(f"{player1.get_name()} is a winner!")
    elif board.get_winner() == player2.get_sign():
        print(f"{player2.get_name()} is a winner!")
    else:
        print("It is a tie!")
    ans = input("Would you like to play again? [Y/N]\n").upper()
    if (ans != "Y"):
        break
print("Goodbye!")


player.py
# Assignment: Programming Assignment 2
# Author: Debi Majumdar
# Date: 2/5/23
# File: player.py is a program that implements different players of a Tic Tac Toe game
# Input: user responses (strings)
# Output: moves on Tic Tac Toe board (strings)

import random
from random import choice


class Player:
    def __init__(self, name, sign):
        self.name = name  # player's name
        self.sign = sign  # player's sign O or X

    def get_sign(self):
        # return an instance sign
        return self.sign

    def get_name(self):
        # return an instance name
        return self.name

    def choose(self, board):
        count = 0
        valid_input = False
        while (valid_input == False):
            if count != 0:  # if not the first time prompting user to choose cell
                print("You did not choose correctly.")
            print(self.name + ", " + self.sign + ": Enter a cell [A-C][1-3]:")  # prompt user to choose cell
            cell_choice = input()
            if type(cell_choice) == str:  # check if input is a 2 character string with a letter A-C and a number 1-3
                if len(cell_choice) == 2:
                    if cell_choice[0] in ["A", "a", "B", "b", "C", "c"] and cell_choice[1] in ["1", "2", "3"]:
                        cell = cell_choice[0].upper() + cell_choice[
                            1]  # make the cell string with uppercase letter A-C and number 1-3
                        if board.isempty(
                                cell) == True:  # if chosen cell has not already been chosen, exit while loop and place sign on cell in board
                            valid_input = True
                            board.set(cell, self.sign)
            count += 1


class AI(Player):
    def __init__(self, name, sign, board):
        self.name = name  # AI's name
        self.sign = sign  # AI's sign
        if self.sign == "X":  # assign opponent's sign to opposite of AI's sign
            self.opponent_sign = "O"
        else:
            self.opponent_sign = "X"
        self.board = board
        self.possible_choices = ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2",
                                 "C3"]  # use list to track which cells are still empty

    def choose(self, board):
        print(self.name + ", " + self.sign + ": Enter a cell [A-C][1-3]:")  # prompt user to choose cell
        for x in self.possible_choices:  # traverse through possible choices list and update it if any cells have been taken
            if board.isempty(x) != True:
                self.possible_choices.remove(x)
        move = random.choice(self.possible_choices)  # choose a random element from possible choices list
        self.possible_choices.remove(move)  # remove the chosen element from possible choices list
        board.set(move, self.sign)  # place AI's sign on cell in board using board.set()
        print(move)  # print the chosen move


class MiniMax(AI):
    def choose(self, board):
        print(f"\n{self.name}, {self.sign}: Enter a cell [A-C][1-3]: ")  # prompt user to choose cell
        for x in self.possible_choices:  # traverse through possible choices list and update it if any cells have been taken
            if board.isempty(x) != True:
                self.possible_choices.remove(x)
        cell = MiniMax.minimax(self, board, True,
                               True)  # call minimax function with MiniMax's turn first to choose optimal move
        print(cell)  # print the chosen move
        self.possible_choices.remove(cell)  # remove the chosen element from possible choices list
        board.set(cell, self.sign)  # place MiniMax's sign on cell in board using board.set()

    def minimax(self, board, self_player, start):
        # check the base conditions
        if board.isdone():
            # self is a winner
            if board.get_winner() == self.sign:
                return 1
            # is a tie
            elif board.get_winner() == "":
                return 0
            # self is a loser (opponent is a winner)
            else:
                return -1

        # set max score to -infinity and min score to infinity
        max_score = float('-inf')
        min_score = float('inf')
        move = ""
        for cell in ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"]:  # traverse through board cells
            if self.board.isempty(cell):  # if cell is empty
                if self_player:  # if it's MiniMax's turn
                    board.set(cell, self.sign)  # place MiniMax's sign on cell in board using board.set()
                    score = MiniMax.minimax(self, board, False,
                                            False)  # call minimax function recursively on opponent's turn
                    if score > max_score:  # compare score to max score and update max score and move
                        max_score = score
                        move = cell

                else:  # if it's opponent's turn
                    board.set(cell, self.opponent_sign)  # place opponent's sign on cell in board using board.set()
                    score = MiniMax.minimax(self, board, True,
                                            False)  # call minimax function recursively on MiniMax's turn
                    if score < min_score:  # compare score to min score and update min score and move
                        min_score = score
                        move = cell

                board.set(cell, " ")  # reset the cell

        if start:  # return move if recursion is done
            return move
        elif self_player:  # return max score on MiniMax's turn
            return max_score
        else:
            return min_score  # return min score on opponent's turn


class SmartAI(AI):
    def choose(self, board):
        print(f"\n{self.name}, {self.sign}: Enter a cell [A-C][1-3]: ")  # prompt user to choose cell
        for x in self.possible_choices:  # traverse through possible choices list and update it if any cells have been taken
            if board.isempty(x) != True:
                self.possible_choices.remove(x)
        move = SmartAI.smart_AI(self, board)  # find next best move using smart_AI()
        print(move)  # print chosen move
        board.set(move, self.sign)  # place AI's sign on cell in board using board.set()

    def smart_AI(self, board):
        if self.sign not in board.board and board.isempty("B2"):  # if available pick center cell for first move
            return "B2"
        else:
            # check for possible chances to win
            for x in range(3):
                value = SmartAI.create_win(self, [3 * x, 1 + (3 * x), 2 + (
                            3 * x)])  # check rows for a possible chance to win using create_win()
                if value != None:  # if there is a row with two of AI's sign and third spot is available, return third spot
                    indexes = ["A1", "B1", "C1", "A2", "B2", "C2", "A3", "B3", "C3"]
                    if indexes[value] in self.possible_choices:
                        return indexes[value]

                value = SmartAI.create_win(self, [x, x + 3,
                                                  x + 6])  # check columns for a possible chance to win using create_win()
                if value != None:  # if there is a column with two of AI's sign and third spot is available, return third spot
                    indexes = ["A1", "B1", "C1", "A2", "B2", "C2", "A3", "B3", "C3"]
                    if indexes[value] in self.possible_choices:
                        return indexes[value]

            value = SmartAI.create_win(self,
                                       [0, 4, 8])  # check diagonal 1 for a possible chance to win using create_win()
            if value != None:  # if diagonal 1 has two of AI's sign and third spot is available, return third spot
                indexes = ["A1", "B1", "C1", "A2", "B2", "C2", "A3", "B3", "C3"]
                if indexes[value] in self.possible_choices:
                    return indexes[value]

            value = SmartAI.create_win(self,
                                       [2, 4, 6])  # check diagonal 2 for a possible chance to win using create_win()
            if value != None:  # if diagonal 2 has two of AI's sign and third spot is available, return third spot
                indexes = ["A1", "B1", "C1", "A2", "B2", "C2", "A3", "B3", "C3"]
                if indexes[value] in self.possible_choices:
                    return indexes[value]

            # check if opponent has chance to win
            for x in range(3):
                value = SmartAI.block_win(self, [3 * x, 1 + (3 * x), 2 + (
                            3 * x)])  # check rows for opponent's possible chance to win using block_win()
                if value != None:  # if there is a row with two of opponent's sign and third spot is available, return third spot
                    indexes = ["A1", "B1", "C1", "A2", "B2", "C2", "A3", "B3", "C3"]
                    if indexes[value] in self.possible_choices:
                        return indexes[value]

                value = SmartAI.block_win(self, [x, x + 3,
                                                 x + 6])  # check columns for opponent's possible chance to win using block_win()
                if value != None:  # if there is a column with two of opponent's sign and third spot is available, return third spot
                    indexes = ["A1", "B1", "C1", "A2", "B2", "C2", "A3", "B3", "C3"]
                    if indexes[value] in self.possible_choices:
                        return indexes[value]

            value = SmartAI.block_win(self, [0, 4,
                                             8])  # check diagonal 1 for opponent's possible chance to win using block_win()
            if value != None:  # if diagonal 1 has two of opponent's sign and third spot is available, return third spot
                indexes = ["A1", "B1", "C1", "A2", "B2", "C2", "A3", "B3", "C3"]
                if indexes[value] in self.possible_choices:
                    return indexes[value]

            value = SmartAI.block_win(self, [2, 4,
                                             6])  # check diagonal 2 for opponent's possible chance to win using block_win()
            if value != None:  # if diagonal 2 has two of opponent's sign and third spot is available, return third spot
                indexes = ["A1", "B1", "C1", "A2", "B2", "C2", "A3", "B3", "C3"]
                if indexes[value] in self.possible_choices:
                    return indexes[value]

            # if opponent has 2 corners already and AI has middle spot, ensure a tie by not selecting a corner and instead selecting middle spot on top row, bottom row, left column, or right column
            if (self.board.board[4] == self.sign and (
                    self.board.board[0] == self.opponent_sign and self.board.board[8] == self.opponent_sign) or (
                    self.board.board[2] == self.opponent_sign and self.board.board[6] == self.opponent_sign)):
                moves = ["A2", "B1", "C2", "B3"]
                for x in moves:
                    if x in self.possible_choices:
                        return move

            # if corner is available, select a corner
            for x in ["A1", "C1", "A3", "C3"]:
                if board.isempty(x) == True:
                    return x

            # if none of the above are true, select a random available cell
            return random.choice(self.possible_choices)

    def block_win(self, indexes):
        # check if opponent has chance to win
        count = 0
        spaces = ['', '', '', '', '', '', '', '', '']
        moves = ["A1", "B1", "C1", "A2", "B2", "C2", "A3", "B3", "C3"]
        for y in indexes:  # go through row, column, or diagonal and check who took which spots
            spaces[y] = 'safe'
            if self.board.board[y] == self.opponent_sign:
                spaces[y] = 'taken'
                count += 1
        if count == 2 and self.board.isempty(
                moves[spaces.index('safe')]):  # if two spots are taken by opponent, return the third spot
            return spaces.index('safe')
        return None  # return None if opponent does not have chance to win

    def create_win(self, indexes):
        # check if AI has chance to win
        count = 0
        spaces = ['', '', '', '', '', '', '', '', '']
        moves = ["A1", "B1", "C1", "A2", "B2", "C2", "A3", "B3", "C3"]
        for y in indexes:  # go through row, column, or diagonal and check who took which spots
            spaces[y] = 'no'
            if self.board.board[y] == self.sign:
                spaces[y] = 'yes'
                count += 1
        if count == 2 and self.board.isempty(
                moves[spaces.index('no')]):  # if two spots are taken by AI, return the third spot
            return spaces.index('no')
        return None  # return None if AI does not have chance to win
      
board.py  
# Assignment: Programming Assignment 2
# Author: Debi Majumdar
# Date: 2/5/23
# File: board.py is a program that implements the Tic Tac Toe board in a game
# Input: user responses (strings)
# Output: Tic Tac Toe board (multiple strings)

class Board:
    def __init__(self):
        # board is a list of cells that are represented by strings (" ", "O", and "X")
        # initially it is made of empty cells represented by " " strings
        self.sign = " "
        self.size = 3
        self.board = list(self.sign * self.size ** 2)
        # the winner's sign O or X
        self.winner = ""

    def get_size(self):
        # return the board size (an instance size)
        return self.size

    def get_winner(self):
        # return the winner's sign O or X (an instance winner)
        return self.winner

    def set(self, cell, sign):
        # convert A1, B1, …, C3 cells into index values from 1 to 9 using a dictionary
        # mark the cell on the board with the sign X or O
        # assign sign to corresponding index in the board list
        indexes = {"A1": 1, "B1": 2, "C1": 3, "A2": 4, "B2": 5, "C2": 6, "A3": 7, "B3": 8, "C3": 9}
        cell_index = indexes[cell] - 1
        self.board[cell_index] = sign

    def isempty(self, cell):
        # convert A1, B1, …, C3 cells into index values from 1 to 9 using a dictionary
        # return True if the cell is empty in board list
        indexes = {"A1": 1, "B1": 2, "C1": 3, "A2": 4, "B2": 5, "C2": 6, "A3": 7, "B3": 8, "C3": 9}
        cell_index = indexes[cell] - 1
        if self.board[cell_index] == " ":
            return True

    def isdone(self):
        done = False
        self.winner = ''

        # check each of the rows in the board
        # if a win is present in a row, assign the variable done to True and the instance var winner to O or X
        if self.board[0] == self.board[1] == self.board[2] == "X" or self.board[0] == self.board[1] == self.board[
            2] == "O":  # first row
            done = True
            self.winner = self.board[0]
        elif self.board[3] == self.board[4] == self.board[5] == "X" or self.board[3] == self.board[4] == self.board[
            5] == "O":  # second row
            done = True
            self.winner = self.board[3]
        elif self.board[6] == self.board[7] == self.board[8] == "X" or self.board[6] == self.board[7] == self.board[
            8] == "O":  # third row
            done = True
            self.winner = self.board[6]

        # check each of the columns in the board
        # if a win is present in a column, assign the variable done to True and the instance var winner to O or X
        elif self.board[0] == self.board[3] == self.board[6] == "X" or self.board[0] == self.board[3] == self.board[
            6] == "O":  # first column
            done = True
            self.winner = self.board[0]
        elif self.board[1] == self.board[4] == self.board[7] == "X" or self.board[1] == self.board[4] == self.board[
            7] == "O":  # second column
            done = True
            self.winner = self.board[1]
        elif self.board[2] == self.board[5] == self.board[8] == "X" or self.board[2] == self.board[5] == self.board[
            8] == "O":  # third column
            done = True
            self.winner = self.board[2]

        # check both diagonals in the board
        # if a win is present in a diagonal, assign the variable done to True and the instance var winner to O or X
        elif self.board[0] == self.board[4] == self.board[8] == "X" or self.board[0] == self.board[4] == self.board[
            8] == "O":  # first diagonal
            done = True
            self.winner = self.board[0]
        elif self.board[2] == self.board[4] == self.board[6] == "X" or self.board[2] == self.board[4] == self.board[
            6] == "O":  # second diagonal
            done = True
            self.winner = self.board[2]

        # check for a tie
        # if all of the spots on the board are taken and previous win conditions are not fulfilled, assign the variable done to True
        # don't change instance var winner from "" to mark tie
        count = 0
        for x in ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"]:
            if self.isempty(x) != True:
                count += 1
        if count == 9:
            done = True

        return done

    def show(self):
        # draw the board
        print("")
        print("   A   B   C  ")
        for x in range(3):
            print(" +---+---+---+")
            print(str(x + 1) + "| " + self.board[3 * x] + " | " + self.board[1 + (3 * x)] + " | " + self.board[
                2 + (3 * x)] + " |")
        print(" +---+---+---+")
        print("")

