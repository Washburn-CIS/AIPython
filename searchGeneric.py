# searchGeneric.py - Generic Searcher, including depth-first and A*
# AIFCA Python code Version 0.9.12 Documentation at https://aipython.org
# Download the zip file and read aipython.pdf for documentation

# Artificial Intelligence: Foundations of Computational Agents https://artint.info
# Copyright 2017-2023 David L. Poole and Alan K. Mackworth
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from display import Displayable

class Searcher(Displayable):
    """returns a searcher for a problem.
    Paths can be found by repeatedly calling search().
    This does depth-first search unless overridden
    """
    def __init__(self, problem):
        """creates a searcher from a problem
        """
        self.problem = problem
        self.initialize_frontier()
        self.num_expanded = 0
        self.add_to_frontier(Path(problem.start_node()))
        super().__init__()

    def initialize_frontier(self):
        self.frontier = []
        
    def empty_frontier(self):
        return self.frontier == []
        
    def add_to_frontier(self,path):
        self.frontier.append(path)
        
    def select_from_frontier(self, frontier):
        """selects a path to explore from the frontier"""
        raise NotImplementedError("choice of serach algorithm implemented here")   # abstract method
        
    def search(self):
        """returns (next) path from the problem's start node
        to a goal node. 
        Returns None if no path exists.
        """
        while not self.empty_frontier():
            self.path = self.select_from_frontier(self.frontier)
            self.num_expanded += 1
            if self.num_expanded % 1000 == 0:
              self.display(1, f"Expanded {self.num_expanded} nodes...\n")
            if self.problem.is_goal(self.path.end()):    # solution found
                self.solution = self.path   # store the solution found
                self.display(1, f"Solution: {self.path} (cost: {self.path.cost})\n",
                    self.num_expanded, "paths have been expanded and",
                            len(self.frontier), "paths remain in the frontier")
                return self.path
            else:
                self.display(4,f"Expanding: {self.path} (cost: {self.path.cost})")
                neighs = self.problem.neighbors(self.path.end())
                self.display(2,f"Expanding: {self.path} with neighbors {neighs}")
                for arc in reversed(list(neighs)):
                    self.add_to_frontier(Path(self.path,arc))
                self.display(3, f"New frontier: {[p.end() for p in self.frontier]}")

        self.display(0,"No (more) solutions. Total of",
                     self.num_expanded,"paths expanded.")

# Depth-first search for problem1; do the following:
# searcher1 = Searcher(searchExample.problem1)
# searcher1.search()  # find first solution
# searcher1.search()  # find next solution (repeat until no solutions)
# searcher_sdg = Searcher(searchExample.simp_delivery_graph)
# searcher_sdg.search()  # find first or next solution

import heapq        # part of the Python standard library
from searchProblem import Path

class FrontierPQ(object):
    """A frontier consists of a priority queue (heap), frontierpq, of
        (value, index, path) triples, where
    * value is the value we want to minimize (e.g., path cost + h).
    * index is a unique index for each element
    * path is the path on the queue
    Note that the priority queue always returns the smallest element.
    """

    def __init__(self):
        """constructs the frontier, initially an empty priority queue 
        """
        self.frontier_index = 0  # the number of items added to the frontier
        self.frontierpq = []  # the frontier priority queue

    def empty(self):
        """is True if the priority queue is empty"""
        return self.frontierpq == []

    def add(self, path, value):
        """add a path to the priority queue
        value is the value to be minimized"""
        self.frontier_index += 1    # get a new unique index
        heapq.heappush(self.frontierpq,(value, -self.frontier_index, path))

    def pop(self):
        """returns and removes the path of the frontier with minimum value.
        """
        (_,_,path) = heapq.heappop(self.frontierpq)
        return path 

    def count(self,val):
        """returns the number of elements of the frontier with value=val"""
        return sum(1 for e in self.frontierpq if e[0]==val)

    def __repr__(self):
        """string representation of the frontier"""
        return str([(n,c,str(p)) for (n,c,p) in self.frontierpq])
    
    def __len__(self):
        """length of the frontier"""
        return len(self.frontierpq)

    def __iter__(self):
        """iterate through the paths in the frontier"""
        for (_,_,path) in self.frontierpq:
            yield path

class Depth_first_searcher(Searcher):
    def select_from_frontier(self, frontier):
        """selects a path to explore from the frontier"""
        return frontier.pop()


class Breadth_first_searcher(Searcher):
    def select_from_frontier(self, frontier):
        """selects a path to explore from the frontier"""
        ret = frontier[0]
        del frontier[0]
        return ret


class Searcher_no_cycles(Searcher):
    def __init__(self, problem):
        self.visited = dict()
        super().__init__(problem)
        
    def add_to_frontier(self, path):
        if path.end() not in self.visited or path.cost < self.visited[path.end()]:
            self.frontier.append(path)
            self.visited[path.end()] = cost

class Breadth_first_searcher_no_cycles(Breadth_first_searcher, Searcher_no_cycles):
    pass

class Depth_first_searcher_no_cycles(Depth_first_searcher, Searcher_no_cycles):
    pass


class A_star_searcher(Depth_first_searcher):
    """returns a searcher for a problem.
    Paths can be found by repeatedly calling search().
    """

    def __init__(self, problem):
        super().__init__(problem)

    def initialize_frontier(self):
        self.frontier = FrontierPQ()

    def empty_frontier(self):
        return self.frontier.empty()

    def add_to_frontier(self,path):
        """add path to the frontier with the appropriate cost"""
        value = path.cost+self.problem.heuristic(path.end())
        self.frontier.add(path, value)


class A_star_searcher_no_cycles(Depth_first_searcher):
    """returns a searcher for a problem.
    Paths can be found by repeatedly calling search().
    """

    def __init__(self, problem):
        self.visited = dict()
        super().__init__(problem)

    def initialize_frontier(self):
        self.frontier = FrontierPQ()

    def empty_frontier(self):
        return self.frontier.empty()

    def add_to_frontier(self,path):
        """add path to the frontier with the appropriate cost"""
        if path.end() not in self.visited or path.cost < self.visited[path.end()]:
            self.visited[path.end()] = path.cost
            self.frontier.add(path, path.cost+self.problem.heuristic(path.end()))


import searchExample

def test(SearchClass, problem=searchExample.problem1, solutions=[['G','D','B','C','A']] ):
    """Unit test for aipython searching algorithms.
    SearchClass is a class that takes a problem and implements search()
    problem is a search problem
    solutions is a list of optimal solutions 
    """
    print("Testing problem 1:")
    schr1 = SearchClass(problem)
    path1 = schr1.search()
    print("Path found:",path1)
    assert path1 is not None, "No path is found in problem1"
    assert list(path1.nodes()) in solutions, "Shortest path not found in problem1"
    print("Passed unit test")

if __name__ == "__main__":
    #test(Depth_first_searcher)      # what needs to be changed to make this succeed?
    test(A_star_searcher)



