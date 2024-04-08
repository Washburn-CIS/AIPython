# agents.py - Agent and Controllers
# AIFCA Python code Version 0.9.12 Documentation at https://aipython.org
# Download the zip file and read aipython.pdf for documentation

# Artificial Intelligence: Foundations of Computational Agents https://artint.info
# Copyright 2017-2023 David L. Poole and Alan K. Mackworth
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from display import Displayable  

class Agent(Displayable):

    def initial_action(self, percept):
        """return the initial action."""
        return self.select_action(percept)   # same as select_action

    def select_action(self, percept):
        """return the next action (and update internal state) given percept
        percept is variable:value dictionary
        """
        raise NotImplementedError("go")   # abstract method

class Environment(Displayable):
    def initial_percept(self, *agents):
        """returns the initial percepts for the agents"""
        raise NotImplementedError("initial_percept")   # abstract method

    def do(self, *action):
        """does the actions in the environment
        returns the next percept """
        raise NotImplementedError("Environment.do")   # abstract method

class Simulator(Displayable): 
    """simulate the interaction between the agent and the environment
    for n time steps.
    Returns a pair of the agent state and the environment state.
    """
    def __init__(self, environment, *agents):
        self.agents = agents
        self.env = environment
        self.percept_history = []
        self.action_history = []
        
    def go(self, n):
        """runs the simulation for 'n' rounds"""
        percepts = self.env.initial_percept(self.agents)
        self.display(2, f"initial percepts: {percepts}")
        self.display(2, f"map: \n{self.env}")
        for i in range(n):
            self.percept_history.append(percepts)
            actions = []
            if i == 0:   # on the first round, use the agent's initial action
                for i in range(len(self.agents)):
                    actions.append(self.agents[i].initial_action(percepts[i]))
                    percepts = self.env.do(actions)
            else:
                for i in range(len(self.agents)):
                    actions.append(self.agents[i].select_action(percepts[i]))
                    percepts = self.env.do(actions)
                    print(percepts)
            self.action_history.append(actions)
            print(self.env)

