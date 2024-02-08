import searchProblem
from searchProblem import Search_problem
from searchProblem import Arc
from searchProblem import Path
import searchGeneric
from searchGeneric import Searcher
from searchGeneric import Breadth_first_searcher
from searchGeneric import Depth_first_searcher
from searchGeneric import Breadth_first_searcher_no_cycles
from searchGeneric import Depth_first_searcher_no_cycles
from searchGeneric import A_star_searcher
import time

default_maze_str = """
***********
* *       *
* *       *
* *       *
* *       *
* *       *
* *       *
* *       *
* *       *
*         *
*         *
*         *
*         *
*         *
***********"""                 

default_goal_state = (13, 1)
#default_goal_state = (13, 9)
default_initial_state = (1, 1)



class Maze_puzzle(Search_problem):
    """An implementation of a sliding n-puzzle (8-puzzle, 15-puzzle, etc)
    """
    
    def __init__(self, initial_state=default_initial_state, maze_def = default_maze_str, goal_state=default_goal_state):
        self.inital_state = initial_state
        self.goal_state = goal_state
        maze_def = maze_def.strip()
        self.passable_coordinates = set()
        rows = maze_def.split('\n')
        self.maze_def = maze_def
        for r in range(len(rows)):
          for c in range(len(rows[r])):
            if rows[r][c] == ' ':
              self.passable_coordinates.add((r, c))
        #print(self.passable_coordinates)
          
    def start_node(self):
        """returns start node"""
        return self.inital_state
    
    def is_goal(self,state):
        """is True if state is a goal"""
        return state == self.goal_state

    def neighbors(self,state):
        """returns a list of the arcs for the neighbors of node"""
        r, c = state
        """
        if (r-1, c) in self.passable_coordinates: # can I travel to (r-1, c) in the maze?
          yield Arc(state, (r-1, c))
        if (r+1, c) in self.passable_coordinates: 
          yield Arc(state, (r+1, c))
        if (r, c-1) in self.passable_coordinates: 
          yield Arc(state, (r, c-1))
        if (r, c+1) in self.passable_coordinates: 
          yield Arc(state, (r, c+1))
        """
        return map(lambda rs: Arc(state, rs),  # make arcs out of each visitable state
                   filter(lambda s: s in self.passable_coordinates, # filter out those we can visit
                          [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]))  # every possible state
                          
    def heuristic(self,n):
        return abs(n[0] - self.goal_state[0]) + abs(n[1] - self.goal_state[1])
          
        
problem = Maze_puzzle()
searcher = Depth_first_searcher(problem)
#searcher = Breadth_first_searcher(problem)
#searcher = Breadth_first_searcher_no_cycles(problem)
#searcher = Depth_first_searcher_no_cycles(problem)
#searcher = A_star_searcher(problem)
start_time = time.perf_counter()
sol = searcher.search()
end_time = time.perf_counter()
print(sol)
print('time: ' + str(end_time-start_time))
