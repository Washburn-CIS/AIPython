# Implementation of tic-tac-toe game tree search 
# Copyright Joseph Kendall-Morwick 2023
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

# https://playtictactoe.org/

from masProblem import Node
from masMiniMax import minimax_alpha_beta

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
    super().__init__(str(move), isMax)
    self.prior_moves = [move] + prior_moves if move else []
    self.board = new_board

    # process move for prior player
    if move:
      token = 'O' if isMax else 'X'
      row = list(new_board[move[1]])
      row[move[0]] = token
      board = list(new_board)
      board[move[1]] = tuple(row)
      self.board = tuple(board)
    
  def children(self):
    """overrides parent method to simply generate child nodes from legal moves"""
    for move in self.legal_moves():
      yield TicTacToe(not self.isMax, move, self.prior_moves, self.board)
  
  def is_leaf(self):
    """in tic-tac-toe, this is a leaf node if there are no moves left or a player has 3 in a row"""
    return len(list(self.legal_moves())) == 0 or self.evaluate() != 0
      
  def legal_moves(self):
    """generates all legal moves (2-tuples of coordinates) for the current board state"""
    for r in range(len(self.board)):
      for c in range(len(self.board[r])):
        if self.board[r][c] == None:
          yield (c, r)
   
  def evaluate(self):
    """returns the evaluation for this node if it is a leaf"""
    def eval3(c1, c2, c3):
      if c1 == c2 and c2 == c3 and c1:  # all values are the same and not blank
        return 1 if row[0] == 'X' else -1
      else:
        return 0
    
    # check each row
    for row in self.board:
      if eval3(row[0], row[1], row[2]):
        return eval3(row[0], row[1], row[2])
    
    # check each col
    for c in range(3):
      if eval3(self.board[0][c], self.board[1][c], self.board[2][c]):
        return  eval3(self.board[0][c], self.board[1][c], self.board[2][c])
    
    #check diagonals
    if eval3(self.board[0][0], self.board[1][1], self.board[2][2]):  
      return eval3(self.board[0][0], self.board[1][1], self.board[2][2])
      
    if eval3(self.board[0][2], self.board[1][1], self.board[2][0]):  
      return eval3(self.board[0][2], self.board[1][1], self.board[2][0])
      
    return 0
    
    
n = TicTacToe(True)

n2 = minimax_alpha_beta(n)
print(n2)










