from deliveryBots import *
from agents import *

env = Delivery_bots_map(simple_map)
agent = Simple_Delivery_Agent()
env.max_display_level = 2
sim = Simulator(agent, env)
env.pretty_print()
sim.go(10)

