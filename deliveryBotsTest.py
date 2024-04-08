from deliveryBots import *
from agents import *
# example
env = Delivery_bots_map(simple_map)
agent0 = Simple_Delivery_Agent()
agent1 = Simple_Delivery_Agent()
env.max_display_level = 2
sim = Simulator(env, agent0, agent1)
sim.go(100)

