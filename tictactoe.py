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


def print_game_board(board):
    v = lambda c: ' ' if not c else c  # draw 'None' as a blank
    print(v(board[0][0])+'|'+v(board[0][1])+'|'+v(board[0][2]))
    print('-----')
    print(v(board[1][0])+'|'+v(board[1][1])+'|'+v(board[1][2]))
    print('-----')
    print(v(board[2][0])+'|'+v(board[2][1])+'|'+v(board[2][2]))


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
    
  def children(self):
    """overrides parent method to simply generate child nodes from legal moves"""
    for move in self.legal_moves():
      yield TicTacToe(not isMax, move, self.prior_moves)
  
  def isLeaf(self):
    """in tic-tac-toe, this is a leaf node if there are no moves left or a player has 3 in a row"""
    return len(self.legal_moves()) == 0 or self.evaluate() != 0
      
  def legal_moves(self):
    """generates all legal moves (2-tuples of coordinates) for the current board state"""
    pass
   
  def evaluate(self):
    """returns the evaluation for this node if it is a leaf"""
    pass

n = TicTacToe(True, (1, 2))
print_game_board(n.board)
