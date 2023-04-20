import random

# load scrabble dictionary
wordsfile = open('data/Collins_Scrabble_Words_2019_.txt')
words = wordsfile.readlines()
words = words[2:]
words = tuple(map(lambda x : x.strip(), words))

def random_word():
  """return a random word from the scrabble dictionary"""
  return random.choice(words)


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
 
