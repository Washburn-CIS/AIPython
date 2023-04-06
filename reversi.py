# Partial implementation of reversi game tree search programming exercises
# Copyright Joseph Kendall-Morwick 2023
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

# https://www.mathsisfun.com/games/reversi.html


from masProblem import Node

# game board states are represented as a 8-tuple of 8-tuples, 
# each containing an 'X', an 'O', or None 
# 'X' is the first (red) player and 'O' is the second (blue) player

initial_game_board = (
  (None,)*8, 
  (None,)*8, 
  (None,)*8, 
  (None, None, None, 'X', 'O', None, None, None),
  (None, None, None, 'O', 'X', None, None, None),
  (None,)*8, 
  (None,)*8, 
  (None,)*8)


def print_game_board(board):
    v = lambda c: '.' if not c else c  # draw 'None' as a dot
    for row in board:
      for col in row:
        print(v(col), end="")
      print("")


class Reversi(Node):
  def __init__(self, isMax=True, move=None, prior_moves=[], new_board=initial_game_board):
    """Initializes game state.
       isMax is true when it is X's turn and false otherwise
       move is a 2-tuple of coordinates on the board (column, row)
       prior_moves is a list of moves taken to reach this game state
       new_board is a game board as described above"""
    super().__init__(str(move), isMax, None, None)
    self.prior_moves = [move] + prior_moves if move else []
    self.board = new_board

    # process move  (todo: flip all newly surrounded pieces)
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
      yield Reversi(not isMax, move, self.prior_moves)
  
  def isLeaf(self):
    """in tic-tac-toe, this is a leaf node if there are no moves left"""
    return len(self.legal_moves()) == 0
      
  def legal_moves(self):
    """generates all legal moves (2-tuples of coordinates) for the current board state"""
    pass # todo: generate legal moves
   
  def evaluate(self):
    """returns the evaluation for this node if it is a leaf"""
    # todo: evaluate leaf node state
    # todo: add heuristic for non-leaf states
    pass 

n = Reversi(True, (4, 2))
print_game_board(n.board)
