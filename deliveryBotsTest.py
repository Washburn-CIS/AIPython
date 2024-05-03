from deliveryBots import *
from deliveryBotsVisualization import *
from agents import *

import tkinter as tk
import PIL
from PIL import Image, ImageTk

game_speed = 10
root = tk.Tk()
root.title("Delivery Bots")    

env = Delivery_bots_visualization(swampy_map, root, 100, 'robot.png', 'robot2.png', 'robot2.png', 'robot2.png')
agent0 = Package_Truck_Agent()
agent1 = Simple_Delivery_Agent()
agent2 = Simple_Delivery_Agent()
agent3 = Simple_Delivery_Agent()
env.max_display_level = 2
sim = Simulator(env, agent0, agent1, agent2, agent3)

def advance():
    sim.go(1)
    root.after(game_speed, advance)

root.after(game_speed, advance)
root.mainloop()
