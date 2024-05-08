from agents import Environment, Agent
import random
import searchProblem
from searchProblem import Search_problem
from searchProblem import Arc
from searchProblem import Path
import searchGeneric
from searchGeneric import Searcher
from searchGeneric import A_star_searcher_no_cycles
import time


class Delivery_map_pathfind(Search_problem):
    
    def __init__(self, initial_state, mapd, goal_state):
        self.inital_state = initial_state
        self.goal_state = goal_state
        self.passable_coordinates = set()
        self.mapd = mapd
        for r,c in mapd.keys():
            if mapd[r,c] in ('.', '!'):
              self.passable_coordinates.add((r, c))
          
    def start_node(self):
        """returns start node"""
        return self.inital_state
    
    def is_goal(self,state):
        """is True if state is a goal"""
        return state == self.goal_state

    def neighbors(self,state):
        """returns a list of the arcs for the neighbors of node"""
        r, c = state
        if (r-1, c) in self.passable_coordinates:
          yield Arc(state, (r-1, c), 1, 'north')
        if (r+1, c) in self.passable_coordinates: 
          yield Arc(state, (r+1, c), 1, 'south')
        if (r, c-1) in self.passable_coordinates: 
          yield Arc(state, (r, c-1), 1, 'west')
        if (r, c+1) in self.passable_coordinates: 
          yield Arc(state, (r, c+1), 1, 'east')
                          
    def heuristic(self,n):
        return abs(n[0] - self.goal_state[0]) + abs(n[1] - self.goal_state[1])
  

class Contestant(Agent):

    def __init__(self, moveProb=0.75, genProb=0.1, valueRange=(1,5)):
        self.moveProb = moveProb
        self.genProb = genProb
        self.valueRange = valueRange
        self.planned_moves = []
        self.package_heat = dict()
        self.packages = dict()
        self.score = 0
        self.bad_packages = set()

    def select_action(self, percept):
        # update basic info
        if 'your_id' in percept:
            self.id = percept['your_id']
            print("\n\nMY NAME IS: ", self.id)
            print(percept)
        if 'locations' in percept:
            self.locations = percept['locations']
            self.location = self.locations[self.id]
            print("LOCATIONS!!",self.location,self.locations)
            
            # remember truck path
            truck_loc = self.locations[0]
            if not truck_loc in self.package_heat:
                self.package_heat[truck_loc] = 1
            else:
                self.package_heat[truck_loc] += 1
            if self.location in self.package_heat:
                del self.package_heat[self.location]
                
        if 'map' in percept:
            self.map = percept['map']
        
        if 'delivered_packages' in percept:
            for dp in percept['delivered_packages']:
                print(percept)
                if dp[0] == self.id:
                    self.score += self.packages[dp[1]][3]
                    del self.packages[dp[1]]
        
        if 'stuck' in percept:
            return 'skip'
            
        if 'pickedup' in percept:
            package = percept['pickedup']
            self.packages[package[0]] = package
            
        if 'packages' in percept:
            if len(self.packages) < 3:
                pchoice = self.choose_package(percept['packages'])
                if pchoice:
                    return 'pickup ' + str(pchoice)
        
        
        # decide to explore or deliver
        if self.planned_moves:
            print(self.planned_moves)
            return self.planned_moves.pop() 

        if self.packages:
            package = random.choice(list(self.packages.values()))
            self.set_path((package[1], package[2]))
        elif self.package_heat:
            self.set_path(max(self.package_heat, key=self.package_heat.get))
            
        return random.choice(('north', 'south', 'east', 'west'))
    
    
    def choose_package(self, packages):
        for package in packages:
            if package[0] in self.bad_packages: continue
            p = self.get_path((package[1], package[2]))
            if not p:
                self.bad_packages.add(package[0])
                continue
            return package[0]
    
    def get_path(self, destination):
        path = []
        problem = Delivery_map_pathfind(self.location, self.map, destination)
        searcher = A_star_searcher_no_cycles(problem)
        start_time = time.perf_counter()
        sol = searcher.search()
        if sol:
            while sol.arc:
                path.append(sol.arc.action)
                sol = sol.initial
        return path

    def set_path(self, destination):
        print("setting dest to ", destination)
        self.planned_moves = self.get_path(destination)
    
