from enum import Enum
import random

# represents types of intersections that can exist in the traffic simulation
class Intersection:
    def canPass() -> bool:
        return
class StopLight(Intersection):
    
    def __init__(self):
        self.y_axis_green = bool(random.randint(0,1))

    def flip_light(self):
        self.y_axis_green = not self.y_axis_green
       
    
class StopSign(Intersection):
    def __init__(self):
        pass
