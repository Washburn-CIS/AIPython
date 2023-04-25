import random
from collections import defaultdict

# load scrabble dictionary
wordsfile = open('data/Collins_Scrabble_Words_2019_.txt')
words = wordsfile.readlines()
words = words[2:]
words = tuple(map(lambda x : x.strip(), words))
    

def read_board(s):
  board = defaultdict(lambda : None)
  y = 0
  for line in s.split("\n"):
    for x in range(len(line)):
      if line[x] != '.' and line[x] != ' ':
        board[x, y] = line[x]
    y += 1
  return board
    
def print_board(board):
  print("  0123456789ABCDEF\n", end="")
  for y in range(15):
    print(hex(y)[-1].upper() + ' ', end="")
    for x in range(15):
      print(board[x, y] if board[x, y] else '.', end="")
    print('')

def combine_bags(b1, b2):
  b = defaultdict(lambda: 0)
  for k in b1:
    b[k] = b1[k]
  for k in b2:
    b[k] = b2[k]
  return b


def random_word():
  """return a random word from the scrabble dictionary"""
  return random.choice(words)

def str_to_bag(s):
  letter_bag = defaultdict(lambda : 0)
  for c in s:
     letter_bag[c] = letter_bag[c] + 1
  return letter_bag

def subbag(s1, s2):
  for c in s1:
    if s1[c] > s2[c]:
      return False
  return True

def get_horizontal_word_at(board, x, y):
  if not board[x, y]: return None
  i = x
  while i>0 and board[i-1,y]: i-=1
  word = ''
  while i<15 and board[i,y]: 
    word += board[i,y]
    i+=1
  return word

def get_vertical_word_at(board, x, y):
  if not board[x, y]: return None
  i = y
  while i>0 and board[x,i-1]: i-=1
  word = ''
  while i<15 and board[x,i]: 
    word += board[x,i]
    i+=1
  return word
  
def legal_move(board, letters, orientation, x, y, word):
  board = board.copy()
  intersects = False
  if orientation == 'across':  
    if x > -1 and board[x-1, y]: intersects = True
    if x + len(word) < 15 and board[x+len(word), y]: intersects = True
    for i in range(len(word)):
      if y > -1 and board[x, y-1]: intersects = True
      if y < 14 and board[x, y+1]: intersects = True
      if board[x+i, y] == '*':
        if letters[word[i]] == 0: return False
        intersects = True
      elif board[x+i, y] and word[i] != board[x+i, y]: return False
      if not board[x+i, y] and letters[word[i]] == 0: return False
      letters[word[i]] -= 1
      board[x+i, y] = word[i]
      newword = get_vertical_word_at(board, x+i, y)
      if len(newword)>1 and newword not in words: return False
    newword = get_horizontal_word_at(board, x, y)
    if newword in words and intersects:
      return board
  if orientation == 'down':
    if y > -1 and board[x, y-1]: intersects = True
    if y + len(word) < 15 and board[x,y+len(word)]: intersects = True
    for i in range(len(word)):
      if x > -1 and board[x-1, y]: intersects = True
      if x < 14 and board[x+1, y]: intersects = True
      if board[x, y+i] == '*':
        if letters[word[i]] == 0: return False
        intersects = True
      elif board[x, y+i] and word[i] != board[x, y+i]: return False
      if not board[x, y+i] and letters[word[i]] == 0: return False
      letters[word[i]] -= 1
      board[x, y+i] = word[i]
      newword = get_horizontal_word_at(board, x, y+i)
      if len(newword)>1 and newword not in words: return False
    newword = get_vertical_word_at(board, x, y)
    if newword in words and intersects:
      return board

def random_move(board, letters, timeout=float('inf')):
  while timeout > 0:
    timeout -=1
    word = random_word()
    orientation = random.choice(('down', 'across'))
    x = random.choice(range(15 - (len(word)-1 if orientation == 'across' else 0)))
    y = random.choice(range(15 - (len(word)-1 if orientation == 'down' else 0)))
    if legal_move(board, letters.copy(), orientation, x, y, word):
         return orientation, x, y, word
      

    
"""  
time_remaining = int(input("Enter remaining time in seconds: "))
yourscore = int(input("Enter your score: "))
opponentscore = int(input("Enter opponent score: "))
print("Enter board state (dots for unoccupied spaces, upper-case letters otherwise): ")
board = ""
for i in range(15):
  board += input()+"\n"
tiles = list(input("Enter player tiles (letters with no spaces): "))

# TODO: determine move
# print one of the following: 
#  pass
#  exchange tiles (where tiles are the tiles to exchange)
#  play orientation x y word
#      Where orientation is either 'down' or 'across'
#      x is in the range 1 through 15 and is the upper-left corner of the word
#      y is in the range 1 through 15 and is the upper-left corner of the word
#      word is the word to be played
"""
boardstr = ("."*15 + "\n")*7 + "."*7 + "*" + "."*7 + "\n" + ("."*15 + "\n")*7
board = read_board(boardstr)
print_board(board)
letters = str_to_bag('AABBCCDDEEFFGGHHIIJJKKLLMMNNOOPPQQRRSSTTUUVVWWXXYYZZ')

# testing code that randomly plays the game with a pretty big letter bag
while True:
  orientation, x, y, word = random_move(board, letters)
  board = legal_move(board, letters.copy(), orientation, x, y, word)
  print_board(board)

#print_board(board)
