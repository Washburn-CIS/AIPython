# Partial implementation of reversi game tree search programming exercises
# Copyright Joseph Kendall-Morwick 2023
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

# https://www.mathsisfun.com/games/reversi.html


from masProblem import Node
from ast import literal_eval
from masMiniMax import minimax_alpha_beta

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
    print('   01234567')	
    for r in range(len(board)):
      row = board[r]
      print(r, ' ', end='')
      for col in row:
        print(v(col), end="")
      print("")

def coordinates_in_range(x, y):
    return x >= 0 and x < 8 and y >= 0 and y < 8

def update_board_from_move(x, y, token, board):
    if not coordinates_in_range(x, y):
      return None
    if board[y][x]:
      return None # space is occupied
    
    opponent_token = 'X' if token == 'O' else 'O'
    move = x, y
    board = list(map(list, board)) # make board modifiable
    valid_move = False
    board[y][x] = token
    for dx in range(-1,2,1):
      for dy in range(-1, 2, 1):
        if not dx and not dy: continue
        # determine if placement would surround opponent tokens
        x, y = move

        while coordinates_in_range(x+dx, y+dy) and board[y+dy][x+dx] == opponent_token:
          x += dx
          y += dy
        
        # capture opponent tokens
        if (x,y) != move and coordinates_in_range(x+dx, y+dy) and board[y+dy][x+dx] == token:
          valid_move = True
          x, y = move
          while coordinates_in_range(x+dx, y+dy) and board[y+dy][x+dx] == opponent_token:
            x += dx
            y += dy
            board[y][x] = token
            
    if valid_move:
      return tuple(map(tuple, board))
        
class Reversi(Node):
  def __init__(self, isMax=True, move=None, prior_moves=[], new_board=initial_game_board):
    """Initializes game state.
       isMax is true when it is X's turn and false otherwise
       move is a 2-tuple of coordinates on the board (column, row)
       prior_moves is a list of moves taken to reach this game state
       new_board is a game board as described above"""
    super().__init__(str(move), isMax)
    self.prior_moves = [move] + prior_moves if move else []
    self.board = new_board
    self.isMax = isMax

    # process move from prior player
    if move:
      token = 'O' if isMax else 'X'
      self.board = update_board_from_move(move[0], move[1], token, new_board)
    
  def children(self):
    """overrides parent method to simply generate child nodes from legal moves"""
    for move in self.legal_moves():
      yield Reversi(not self.isMax, move, self.prior_moves, self.board)
  
  def is_leaf(self):
    """in tic-tac-toe, this is a leaf node if there are no moves left"""
    if list(self.legal_moves()): # not a leaf if we can make a move
      return False
    nn = Reversi(not self.isMax, None, self.prior_moves, self.board) 
    return not list(nn.legal_moves()) # game over if neither we nor opponent can move
      
  def legal_moves(self):
    """generates all legal moves (2-tuples of coordinates) for the current board state"""
    for x in range(8): 
      for y in range(8): # check every tile to see if it is a legal move
        if not self.board[y][x] and update_board_from_move(x, y, 'X' if self.isMax else 'O', self.board):
          yield (x, y)
   
  def evaluate(self):
    """returns the evaluation for this node if it is a leaf"""
    # todo: evaluate leaf node state
    # todo: add heuristic for non-leaf states
    return 0 



a = (
  ('X',)*8, 
  ('X',)*8, 
  ('X',)*8, 
  ('X',)*8, 
  ('X',)*8, 
  ('X',)*8, 
  ('X',)*8, 
  ('O','X','X','X','X',None,None,None))

n = Reversi(new_board=a)
print(list(n.legal_moves()))

"""
print_game_board(n.board)
print('----')
n = Reversi(not n.isMax, (3, 5), [], n.board)
print_game_board(n.board)
n = Reversi(not n.isMax, (4, 5), [], n.board)
print_game_board(n.board)
n = Reversi(not n.isMax, (5, 3), [], n.board)
print_game_board(n.board)
n = Reversi(not n.isMax, (4, 2), [], n.board)
print_game_board(n.board)
"""
while not n.is_leaf():
  print_game_board(n.board)
  if not n.isMax:
    if list(n.legal_moves()):
      move = literal_eval(input("enter move: "))
      n = Reversi(True, move, n.prior_moves, n.board)
    else:
      print('player must pass')
      n = Reversi(True, None, n.prior_moves, n.board)
  else:
    res = minimax_alpha_beta(n, max_depth=4)[1]
    if res:
      print(res)
      move = literal_eval(res[0])
      n = Reversi(False, move, n.prior_moves, n.board)
    else:
      print('computer must pass')
      n = Reversi(False, None, n.prior_moves, n.board)

print('final state:')
print_game_board(n.board)
print(n.evaluate())
