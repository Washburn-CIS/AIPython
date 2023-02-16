import searchProblem
from searchProblem import Search_problem
from searchProblem import Arc
from searchProblem import Path
import searchGeneric
from searchGeneric import Searcher
from searchGeneric import BreadthFirstSearcher
from searchGeneric import BreadthFirstSearcherNoCycles
from searchGeneric import AStarSearcher

default_maze_str = """
**********
*        *
* ********
* ****** *
* * *    *
* * * ** *
* * * ** *
* * **** *
*        *
**********"""             

default_goal_state = (1, 8)
default_initial_state = (3, 8)



class MazePuzzle(Search_problem):
    """An implementation of a sliding n-puzzle (8-puzzle, 15-puzzle, etc)
    """
    
    def __init__(self, initial_state=default_initial_state, maze_def = default_maze_str, goal_state=default_goal_state):
        self.inital_state = initial_state
        self.goal_state = goal_state
        maze_def = maze_def.strip()
        self.passable_coordinates = set()
        rows = maze_def.split('\n')
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
          
        
problem = MazePuzzle()
searcher = BreadthFirstSearcherNoCycles(problem)
sol = searcher.search()
print(sol)
