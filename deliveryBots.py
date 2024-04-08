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

from agents import Environment, Agent
import random

# example map description
# dictionary of:
#    'map' -> String: see Delivery_bots_map constructor docstring
#    'package' -> Tuple_of(4-Tuple_of integer): see Delivery_bots_map constructor docstring
simple_map = {
  'map': """...*
!##.
...*""",
  'packages': ((2,0,0,0,1),)
}

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
                + A '*' character is where an agent will start
           'packages': a tuple of 5-tuples of integers including, in order: 
                    a pair of coordinates (row, column) of package location and destination
                    the value of the package when delivered
        """
        self.stuck = set()
        self.package_num = 1
        self.packages = {}
        for p in map['packages']:
            self.packages[self.package_num] = p
            self.package_num += 1
        self.map = dict()
        rows = map['map'].split('\n')   	# split map up in to single strings
        self.rows = len(rows)
        self.cols = len(rows[0])
        self.agent_locations = []
        
        for r in range(len(rows)):          	# for every row
            for c in range(len(rows[r])):	# and every column within the row
                tile = rows[r][c]		# find the tile type
                if tile == '*':			# convert starting locations to passable tiles
                    self.agent_locations.append((r, c))
                    tile = '.'
                self.map[r, c] = tile	# record the tile in the tiles dictionary

    def initial_percept(self, agents):
        """returns the initial percept for the agent
        
           agents should be a list of agents that will operate over the environment.
        
           additional percepts will be delivered to the agent during execution of the 'do'
           method. Percepts will always be a dictionary with string keys. Below is a description
           of the keys and values associated with those keys in a percept:

           key: 'map'
               a 2-d tuple of characters representing tiles on the map. Coordinates of those tiles
               will begin at 0 and will be in row, column order. Characters used will denote the following:
                   '#' - impassable tile
                   '!' - hazardous tile
                   '.' - passable tile
           
           key: 'your_id'
               An integer representing the ID of the agent receiving the percept
           
           key: 'locations'
               A list of 2-d tuples indicating the location of all of the agents in the 
               simulation. Indexes are ID's and locations are (row, column).
               
           key: 'packages'  a list of 4-tuples of integers describing packages:
               ID
               destination row
               destination column
               value
           
           key: 'delivered_packages' a list of 2-tuples of agent id and package id
           key: 'other_agent'   ***TODO
           
        """
        self.agents = agents
        self.stuck = [False]*len(agents)
        self.held_packages = [[]]*len(agents)
        self.scores = [0]*len(agents)
        percepts = []
        for i in range(len(agents)):
            percept = {}
            packages = self.get_packages_on_tile(self.agent_locations[i][0], self.agent_locations[i][1])
            if packages:
                percept['packages'] = \
                    [(i, 
                      self.packages[i][2], 
                      self.packages[i][3], 
                      self.packages[i][4]) for i in packages]
            percept['map'] = self.map
            percept['your_id'] = i
            percept['locations'] = self.agent_locations
            percepts.append(percept)
        return percepts
                 
    def __repr__(self):
        rep = ""
        package_locations = [(p[0], p[1]) for p in self.packages.values()]
        for r in range(self.rows):
            for c in range(self.cols):
                if (r,c) in self.agent_locations:
                    rep += str(self.agent_locations.index((r,c)))
                elif (r,c) in package_locations:
                    rep += '@'
                else:
                    rep += self.map[(r,c)]
            rep += '\n'
        return rep
    
    def get_packages_on_tile(self, r, c):
        return [i for i,p in self.packages.items() if p[0] == r and p[1] == c]
    
    def do(self, actions):
        """allows agents to move around the map and deliver packages
           actions is a list of one of the following strings: 
           
           action: 'north'  -- moves the agent one tile north (if possible)
           action: 'east'  -- moves the agent one tile north (if possible)
           action: 'south'  -- moves the agent one tile north (if possible)
           action: 'west'  -- moves the agent one tile north (if possible)
           action: 'pickup <package number>' -- picks up package with the given number

           actions should arrive in the same order of the agents in the initial_percept call
        """
        
        percepts = []
        delivered_packages = []
        
        for i in range(len(self.agents)):
            agent = self.agents[i]
            action = actions[i]
            percept = {}
            self.display(2, f"agent {i} is currently at {self.agent_locations[i][0]}, {self.agent_locations[i][1]}")
            self.display(2, f"agent {i} issued action: {action}")
            
            # find packages on tile
            packages = self.get_packages_on_tile(self.agent_locations[i][0], self.agent_locations[i][1])
            
            # if the agent got stuck on the previous turn, unstick it and ignore its command
            if self.stuck[i]:
                self.stuck[i] = False
                action = 'skip'
        
            # determine the location the agent wants to travel to
            dest = None
            if action == 'north':
              dest = self.agent_locations[i][0] - 1, self.agent_locations[i][1]
            elif action == 'south':
              dest = self.agent_locations[i][0] + 1, self.agent_locations[i][1]
            elif action == 'east':
              dest = self.agent_locations[i][0], self.agent_locations[i][1] + 1
            elif action == 'west':
              dest = self.agent_locations[i][0], self.agent_locations[i][1] - 1
          
            if dest and dest in self.map:  # if the destination is valid...
                if self.map[dest] == '.':		# passable tile
                    self.agent_locations[i] = dest	# update agents location
                    self.display(2, f"agent is now at {self.agent_locations[i][0]}, {self.agent_locations[i][1]}")

                elif self.map[dest] == '!':		# hazard tile
                    self.display(2, "agent got stuck")
                    self.stuck[i] = True		# agent will be stuck next turn
                    self.agent_locations[i] = dest		# update agents location
                    self.display(2, f"agent is now at {self.agent_locations[i][0]}, {self.agent_locations[i][1]}")

                # other tiles are considered impassable for now, no update to agent
                else:
                    self.display(2, "agent issued invalid move")
                    percept['error'] ='INVALID_MOVE'
                   
            elif len(action) > 7 and action[0:7] == 'pickup ':
                # TODO: check for multiple robots picking up the same package -- assign randomly
                pnum = int(action[7:])
                if pnum in packages and len(self.held_packages[i]) <4:
                    p = self.packages[pnum]
                    del self.packages[pnum]
                    percept['pickedup'] = (pnum, p[2], p[3], p[4])
                    self.held_packages[i].append((pnum, p[2], p[3], p[4]))
                    self.display(2, f"agent {i} picked up package {pnum}")
                else: 
                    self.display(2, "agent issued invalid move")
                    percept['error'] ='INVALID_MOVE'
                
            elif action != 'skip':
                self.display(2, "agent issued invalid move")
                percept['error'] ='INVALID_MOVE'
                
            
            # deliver packages if possible
            for p in self.held_packages[i]:
                if (p[1], p[2]) == (self.agent_locations[i][0], self.agent_locations[i][1]):
                    self.scores[i] += p[3]
                    self.held_packages[i].remove(p)
                    self.display(2, f"agent {i} delivered package {p[0]}")
                    delivered_packages.append((i, p[0]))
            
            # notify packages on tile
            packages = self.get_packages_on_tile(self.agent_locations[i][0], self.agent_locations[i][1])
            if packages:
                percept['packages'] = \
                    [(i, 
                      self.packages[i][2], 
                      self.packages[i][3], 
                      self.packages[i][4]) for i in packages]
            percepts.append(percept)
        
        # inform all agents of delivered packages
        if delivered_packages:
            for p in percepts:
                p['delivered_packages'] = delivered_packages
                
        # inform all agents of all agent movements
        for p in percepts:
            p['locations'] = self.agent_locations
                
        return percepts   


# TODO: develop a web-based log visualizer for deliverybots

class Simple_Delivery_Agent(Agent):

    def select_action(self, percept):
        #TODO: this does not fully implement the assignment. 
        #      you should update the code to avoid obstacles
        if 'packages' in percept: # pickup a package whenever available
            pnum = percept['packages'][0][0]
            return 'pickup ' + str(pnum)
            
        return random.choice(('north', 'south', 'east', 'west'))
    

    
    
