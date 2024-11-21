from traffic_simulation import TrafficSimulation
import time
from constants import *

# AI function will go in this file where we will simulate the game. We can think of the game as a black box.
# We will simply pass in inputs to the simulation and we will get some answer that we then try to minimize.

#TODO 
#Inputs: 
# # the AI inputs are the matrix of stoplights and stopsigns
# for a 3 by 3 intersection
#example [0 ,1, 0]
#        [0, 1, 1]
#        [0, 1  0]
# where 1 represents a stoplight and 0 represents a stopsign
#Output: Avg time to get to destination

# function for runnning the game

# instantiates a traffic simulation and runs it until all cars are at their destination. 
# routes are randomized so the simulation is different each time
# returns the average time to destination

def simulate(ai_inputs):
    ts = TrafficSimulation(matrix=ai_inputs, num_of_cars=10)
    while True:        
        ts.update_car_positions()
        if ts.done():
            result = ts.result()
            break
    return result