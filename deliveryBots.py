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
# Package truck will be agent 0
# packages have a value (integer > 0)
# goal of the game is get the most delivery value
# robots can hold a maximum of 3 packages
# agents can be sensed globally
# agents have an ID
# packages have an ID
# packages are automatically delivered when an agent arrives at their destination
# add "pickup <package num> command
# robots sense scores at all times
# robots sense # of unclaimed packages at all times 
# if two robots attempt to pick up the same package at the same time, result will be uniformly random

from agents import Environment, Agent
import random

# example map description
# dictionary of:
#    'map' -> String: see Delivery_bots_map constructor docstring
#    'package' -> Tuple_of(5-Tuple_of integer): see Delivery_bots_map constructor docstring
simple_map = {
  'map': """...*
!##.
...*""",
  'packages': ((2,0,0,0,1),)
}

test_map = {
  'map': """.###
.###
..**""",
  'packages': ((2,0,0,0,1),)
}

versus_map = {
  'map': """###########
#....*....#
#.........#
#####.#####
#.........#
#....#....#
#*...#...*#
###########""",
  'packages': ((6,1,1,1,10),(6,9,1,9,10))
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
           
        """
        self.agents = agents
        self.stuck = [False]*len(agents)
        self.held_packages = [list() for x in [[]]*len(agents)]
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
    
    
    def update_tile(self, r, c):
        """abstract method called whenever the details of a tile have been updated.
        Used for visualization."""
        pass
    
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
        updated_tiles = set()
        wanted_packages = {}
        
        for i in range(len(self.agents)): # develop percept and handle action for each agent
            agent = self.agents[i]
            action = actions[i]
            percept = {}
            self.display(2, f"agent {i} is currently at {self.agent_locations[i][0]}, {self.agent_locations[i][1]}")
            self.display(2, f"agent {i} is carrying out action: {action}")
            
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
                    updated_tiles.add(self.agent_locations[i])
                    updated_tiles.add(dest)
                    self.agent_locations[i] = dest	# update agents location
                    self.display(2, f"agent is now at {self.agent_locations[i][0]}, {self.agent_locations[i][1]}")

                elif self.map[dest] == '!':		# hazard tile
                    updated_tiles.add(self.agent_locations[i])
                    updated_tiles.add(dest)
                    self.display(2, "agent got stuck")
                    self.stuck[i] = True		# agent will be stuck next turn
                    self.agent_locations[i] = dest		# update agents location
                    self.display(2, f"agent is now at {self.agent_locations[i][0]}, {self.agent_locations[i][1]}")

                # other tiles are considered impassable for now, no update to agent
                else:
                    self.display(2, "agent issued invalid move")
                    percept['error'] ='INVALID_MOVE'
                   
            elif len(action) > 7 and action[0:7] == 'pickup ':
                pid = int(action[7:])
                if pid in packages and len(self.held_packages[i]) <4:
                    if pid not in wanted_packages:
                        wanted_packages[pid] = [i]
                    else: 
                        wanted_packages[pid].append(i)
                    updated_tiles.add(self.agent_locations[i])
                else: 
                    self.display(2, "agent issued invalid move")
                    percept['error'] ='INVALID_MOVE'
            elif len(action) > 9 and action[0:9] == 'generate ' and i==0:
                # agent 0 is  package truck for now, can generate packages
                tokens = action.split(' ')
                value = int(tokens[1])
                self.packages[self.package_num] = (
                    self.agent_locations[i][0], 
                    self.agent_locations[i][1],
                    random.randint(0, self.rows-1),
                    random.randint(0, self.cols-1),
                    value)
                self.package_num += 1
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
            
            
            percepts.append(percept)
            
        
        # inform all agents of delivered packages
        if delivered_packages:
            for p in percepts:
                p['delivered_packages'] = delivered_packages
                
        # inform all agents of all agent movements
        for p in percepts:
            p['locations'] = self.agent_locations
            
            
            
            
        # determine who gets disputed packages and resolve pickup commands
        for pid in wanted_packages:
            self.display(2, f"package {pid} is wanted by agents: {wanted_packages[pid]}")
            aid = random.choice(wanted_packages[pid])
            p = self.packages[pid]
            del self.packages[pid]
            updated_tiles.add(self.agent_locations[aid])
            percepts[aid]['pickedup'] = (pid, p[2], p[3], p[4])
            self.held_packages[aid].append((pid, p[2], p[3], p[4]))
            self.display(2, f"agent {aid} picked up package {pid}")
        
        
        
        # notify each agent of packages on tile 
        for i in range(len(self.agents)): 
            agent_location = (self.agent_locations[i][0], self.agent_locations[i][1])
            self.display(2, f"agent {i} looking for packages on {agent_location}")
            packages = self.get_packages_on_tile(agent_location[0], agent_location[1])
            if packages:
                self.display(2, f"found these: {packages}")
                percepts[i]['packages'] = \
                    [(i, 
                      self.packages[i][2], 
                      self.packages[i][3], 
                      self.packages[i][4]) for i in packages]
            
            
        
        # inform all agents of current scores
        for p in percepts:
            p['scores'] = self.scores
            
        for r,c in updated_tiles:
            self.update_tile(r, c)
        
        return percepts   

class Simple_Delivery_Agent(Agent):

    def select_action(self, percept):
        #TODO: this does not fully implement the assignment. 
        #      you should update the code to avoid obstacles
        if 'packages' in percept: # pickup a package whenever available
            pnum = percept['packages'][0][0]
            return 'pickup ' + str(pnum)
            
        return random.choice(('north', 'south', 'east', 'west'))
    
class Test_Agent(Agent):
    def __init__(self, *actions):
        self.actions = list(actions)
        self.actions.reverse()

    def select_action(self, percept):
        return self.actions.pop() if self.actions else 'skip'
    
class Package_Truck_Agent(Agent):

    def __init__(self, moveProb=0.75, genProb=0.1, valueRange=(1,5)):
        self.moveProb = moveProb
        self.genProb = genProb
        self.valueRange = valueRange

    def select_action(self, percept):
        if random.random() < self.moveProb:  
            return random.choice(('north', 'south', 'east', 'west'))
        if random.random() < self.genProb:
            return 'generate ' + str(random.randint(self.valueRange[0], self.valueRange[1]))
        return 'skip'
    

    
    
