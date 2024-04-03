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

x_is_human = False
o_is_human = False
max_depth=4

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
    assert coordinates_in_range(x, y)
    assert not board[y][x]
    
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
  def __init__(self, isMax=True, player='X', move=None, prior_moves=[], new_board=initial_game_board):
    """Initializes game state.
       isMax is true when it is player's turn and false otherwise
       player is 'X' or 'O' (the player considering a move)
       move is a 2-tuple of coordinates on the board (column, row) made by the last player
       prior_moves is a list of moves taken to reach this game state
       new_board is a game board as described above"""
    super().__init__(str(move), isMax)
    self.prior_moves = [move] + prior_moves if move else []
    self.board = new_board
    self.isMax = isMax
    self.player = player
    self.other_player = 'X' if player == 'O' else 'O'
    
    # validate input
    assert len(self.board) == 8
    for row in self.board:
      assert len(row)==8

    # process move from prior player
    if move:
      assert coordinates_in_range(move[0], move[1])
      player_making_move = self.other_player if self.isMax else self.player
      self.board = update_board_from_move(move[0], move[1], player_making_move, new_board)
      assert self.board, f"invalid move: {player_making_move}:{move} on {new_board}"
    
  def children(self):
    """overrides parent method to simply generate child nodes from legal moves"""
    any_moves = False
    for move in self.legal_moves():
      any_moves = True
      yield Reversi(not self.isMax, self.player, move, self.prior_moves, self.board)
    if not any_moves:
      nn = Reversi(not self.isMax, self.player, None, self.prior_moves, self.board)
      if nn.legal_moves(): # game not over since opponent can play
        yield nn
  
  def is_leaf(self):
    """in tic-tac-toe, this is a leaf node if there are no moves left"""
    if list(self.legal_moves()): # not a leaf if we can make a move
      return False
    nn = Reversi(not self.isMax, self.player, None, self.prior_moves, self.board) 
    return not list(nn.legal_moves()) # game over if neither we nor opponent can move
      
  def legal_moves(self):
    """generates all legal moves (2-tuples of coordinates) for the current board state"""
    for x in range(8): 
      for y in range(8): # check every tile to see if it is a legal move
        if not self.board[y][x] and update_board_from_move(x, y, self.player if self.isMax else self.other_player, self.board):
          yield (x, y)
   
  def evaluate(self):
    """returns the evaluation for this node if it is a leaf"""
    # todo: evaluate leaf node state
    # todo: add heuristic for non-leaf states
    return self.evaluateX() if self.player == 'X' else self.evaluateO()
  
  def evaluateX(self):
    dif = 0
    if self.is_leaf():  # determine winning margin
      for r in self.board:
         for c in r: 
           if self.player == c:
             dif += 1
           elif self.other_player == c:
             dif -= 1
    return dif

    
  def evaluateO(self):
    dif = 0
    if self.is_leaf():  # determine winning margin
      for r in self.board:
         for c in r: 
           if self.player == c:
             dif += 1
           elif self.other_player == c:
             dif -= 1
    return dif
     
           
n = Reversi()
while not n.is_leaf():
    print(f"{n.player}\'s turn")
    print_game_board(n.board)
    print("legal moves:", list(n.legal_moves()))
    if list(n.legal_moves()):
      is_human = (n.player == 'X' and x_is_human) or (n.player == 'O' and o_is_human)
      if is_human:
        move = literal_eval(input("enter move: "))
      else:
        res = minimax_alpha_beta(n, max_depth=max_depth)
        res = res[1]
        print('computer chooses', res[0])
        move = literal_eval(res[0])
      n = Reversi(True, 'X' if n.player == 'O' else 'O', move, n.prior_moves, n.board)
    else:
      print('player must pass')
      n = Reversi(True, 'X' if n.player == 'O' else 'O', None, n.prior_moves, n.board)

print('final state:')
print_game_board(n.board)
dif = 0
for r in n.board:
  for c in r:
    if c == 'X':
      dif += 1
    elif c == 'O':
      dif -= 1
if dif == 0:
  print("Tie")
elif dif > 0:
  print("X wins")
else:
  print("O wins")

