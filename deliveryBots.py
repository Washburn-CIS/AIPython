# deliveryBots.py - Agent and Controllers
# This file contains code to implement an AI-friendly game for 
# use with AIPython. See repository readme for more information
# on that library

# Copyright 2024 Joseph Kendall-Morwick
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en


# Game Rules
# Game environments will have the following attributes:
#  * The environment will consist of a rectangular collection of square tiles
#  * tiles will be passable, impassable, or hazardous
#  * hazadarous tiles will result in a loss of turn for the player
#  * each player will start with a package
#  * packages will have map coordinates for a delivery location
#  * agents can deliver the package when present on the delivery location on a turn
#  * agents are present on a tile at the start of the game
#  * agents can move to adjacent passable tiles on a turn

from agents import Environment

# example map description
simple_map = """@...
!##.
...*"""

class Delivery_bots_map(Environment):

    def __init__(self, map):
        """initializes the game environment
           map is a string with multiple lines
             - each line represents a row in the map
             - each character in a line represents a tile in the map
                + A '.' character is a passable tile
                + A '#' character is an impassable tile
                + A '!' character is a hazardous tile
                + A '*' character is where the agent will start
                + A '@' character is the location where the package must be delivered
        """
        self.stuck = False
        self.map = dict()
        rows = map.split('\n')   	# split map up in to single strings
        for r in range(len(rows)):          	# for every row
            for c in range(len(rows[r])):	# and every column within the row
                tile = rows[r][c]		# find the tile type
                if tile == '*':			# convert starting locations to passable tiles
                    self.robot = (r, c)
                    tile = '.'
                elif tile == '@':		# convert destinations to passable tiles
                    self.package_dest = (r, c)
                    tile = '.'
                self.map[r, c] = rows[r][c]	# record the tile in the tiles dictionary
                
        print(self.map)

    def initial_percept(self):
        """returns the initial percept for the agent"""
        return { 'map': self.map, 
                 'package_dest': self.package_dest, 
                 'location': self.robot}
    
    def do(self, action):
        """allows agents to move around the map and deliver packages
           actions are one of the following strings: north, south, east, west, and deliver"""
        
        # if the agent got stuck on the previous turn, unstick it and ignore its command
        if self.stuck:
            self.stuck = False
            return {}
        
        # determine the location the agent wants to travel to
        dest = None
        if action == 'north':
          dest = self.robot[0] - 1, self.robot[1]
        elif action == 'south':
          dest = self.robot[0] + 1, self.robot[1]
        elif action == 'east':
          dest = self.robot[0], self.robot[1] + 1
        elif action == 'west':
          dest = self.robot[0], self.robot[1] - 1
          
        if dest and dest in self.map:  # if the destination is valid...
            if self.map[dest] == '.':		# passable tile
                self.robot = dest		# update agents location
                return {'location': dest}	# inform agent of state change
            elif self.map[dest] == '!':		# hazard tile
            	self.stuck = True		# agent will be stuck next turn
                self.robot = dest		# update agents location
                return {'location': dest}	# inform agent of state change
            # other tiles are considered impassable for now, no update to agent
        else:
            return {'location': self.robot, 'error': 'INVALID_MOVE'}
                  
    
    
    
    
    
    
    
    
    
    
    
    
