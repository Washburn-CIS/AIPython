from deliveryBots import *
from deliveryBotsVisualization import *
from agents import *

import tkinter as tk
import PIL
from PIL import Image, ImageTk


root = tk.Tk()
root.title("Delivery Bots")    

env = Delivery_bots_visualization(simple_map, root, 100, 'robot.png', 'robot2.png')
agent0 = Package_Truck_Agent()
agent1 = Simple_Delivery_Agent()
env.max_display_level = 2
sim = Simulator(env, agent0, agent1)

def advance():
    sim.go(1)
    root.after(1000, advance)

root.after(1000, advance)
root.mainloop()
