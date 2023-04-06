# Implementation of tic-tac-toe game tree search 
# Copyright Joseph Kendall-Morwick 2023
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

# https://playtictactoe.org/

from masProblem import Node

# game board states are represented as a 3-tuple of 3-tuples, 
# each containing an 'X', an 'O', or None 

initial_game_board = (((None,)*3),)*3


def print_game_board(state):
    v = lambda c: ' ' if not c else c  # draw 'None' as a blank
    print(v(state[0][0])+'|'+v(state[0][1])+'|'+v(state[0][2]))
    print('-----')
    print(v(state[1][0])+'|'+v(state[1][1])+'|'+v(state[1][2]))
    print('-----')
    print(v(state[2][0])+'|'+v(state[2][1])+'|'+v(state[2][2]))


class TicTacToe(Node):
  def __init__(self, isMax=True, move=None, prior_moves=[], new_board=initial_game_board):
    """Initializes game state.
       isMax is true when it is X's turn and false otherwise
       move is a 2-tuple of coordinates on the board (column, row)
       prior_moves is a list of moves taken to reach this game state
       new_board is a game board as described above"""
    super().__init__(str(move), isMax, None, None)
    self.prior_moves = [move] + prior_moves if move else []
    self.board = new_board

    # process move
    if move:
      token = 'X' if isMax else 'O'
      row = list(new_board[move[1]])
      row[move[0]] = token
      board = list(new_board)
      board[move[1]] = tuple(row)
      self.board = tuple(board)


n = TicTacToe(True, (1, 2))
print_game_board(n.board)
