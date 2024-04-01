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


# TODO: add heading
# TODO: add turn comands
# TODO: can view packages within cone vision (3 forward, triangle)

# Package truck moves around and drops packages but has hidden strategy
# possibly more than one truck
# packages have a value (integer > 0)
# goal of the game is get the most delivery value
# robots can hold a maximum of 3 packages
# agents can be sensed within 10 squares manhattan distance
# agents have a type (truck/robot) and a ID
# packages have an ID
# deliver command delivers all packages meant for current destination
# add "pick up <package num> command
# robots sense scores at all times
# robots sense # of unclaimed packages at all times 
# if two robots attempt to pick up the same package at the same time, result will be uniformly random
# TODO: fully describe map format
# TODO: fully describe percept format
# TODO: complete tile types (from discussion board)
# TODO: determine multi-player semantics (from discussion board)
# TODO: determine additional agents (from discussion board)


from agents import Environment, Agent
import random

# example map description
simple_map = """@...
!##.
...*"""

class Delivery_bots_map(Environment):

    def __init__(self, map):
        """initializes the game environment
        
        map is a dictionary with the following properties:
           'map': a string with multiple lines
             - each line represents a row in the map
             - each character in a line represents a tile in the map
                + A '.' character is a passable tile
                + A '#' character is an impassable tile
                + A '!' character is a hazardous tile
                + A '*' character is where the agent will start
                + A '@' character is the location where the package must be delivered
           'portals': a tuple of 2-tuples of coordinates (2-tuples of integers). 
             - each pair of coordinates identifies two portal tiles that are linked 
           'packages': ***
        """
        self.stuck = False
        self.map = dict()
        rows = map.split('\n')   	# split map up in to single strings
        self.rows = len(rows)
        self.cols = len(rows[0])
        
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
        """returns the initial percept for the agent
        
           additional percepts will be delivered to the agent during execution of the 'do'
           method. Percepts will always be a dictionary with string keys. Below is a description
           of the keys and values associated with those keys in a percept:

           key: 'map'
               a 2-d tuple of characters representing tiles on the map. Coordinates of those tiles
               will begin at 0 and will be in row, column order. Characters used will denote the following:
                   '#' - impassable tile
                   '!' - hazardous tile
                   '.' - passable tile
           
           key: 'location'
               A 2-d tuple indicating the location of the tile the agent is located on (row, column).
               
           key: 'portal'
               A list of 2-tuples of coordinates (2-tuples of integers); endpoints of bi-directional
               portals. For example: [((1,1),(2,2)), ((4,5), (0,1))] indicates that
               there are four portals and that stepping on to 1,1 will cause a robot to appear at 
               (2,2), stepping on to (2,2) will cause a robot to appear at (1,1), stepping on (4,5)
               will cause a robot to appear at (0,1) and stepping on to (0,1) will cause a robot
               to appear at (4,5). 
               
           key: 'package_dest'  ***TODO
           
           key: 'other_agent'   ***TODO
           
        """
        return { 'map': self.map, 
                 'package_dest': self.package_dest, 
                 'location': self.robot}
                 
    def pretty_print(self):
        for r in range(self.rows):
            for c in range(self.cols):
                print(self.map[(r,c)], end='')
            print('')
    
    def do(self, action):
        """allows agents to move around the map and deliver packages
           actions are one of the following strings: 
           
           action: 'north'  -- moves the agent one tile north (if possible)
           action: 'east'  -- moves the agent one tile north (if possible)
           action: 'south'  -- moves the agent one tile north (if possible)
           action: 'west'  -- moves the agent one tile north (if possible)
           action: 'deliver'  -- drops package held by the agent ***TODO

        """
        
        self.display(2, f"robot is currently at {self.robot[0]}, {self.robot[1]}")
        self.display(2, "robot issued action: " + action)
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
                self.display(2, f"robot is now at {self.robot[0]}, {self.robot[1]}")
                return {'location': dest}	# inform agent of state change
            elif self.map[dest] == '!':		# hazard tile
                self.display(2, "robot got stuck")
                self.stuck = True		# agent will be stuck next turn
                self.robot = dest		# update agents location
                self.display(2, f"robot is now at {self.robot[0]}, {self.robot[1]}")
                return {'location': dest}	# inform agent of state change
            # other tiles are considered impassable for now, no update to agent
        else:
            self.display(2, "robot issued invalid move")
            return {'location': self.robot, 'error': 'INVALID_MOVE'}
                  
    
    
class Simple_Delivery_Agent(Agent):

    def select_action(self, percept):
        #TODO: this does not fully implement the assignment. 
        #      you should update the code to avoid obstacles
        return random.choice(('north', 'south', 'east', 'west'))
    
    
    
# TODO: *** add package truck agent class
    
    
    
