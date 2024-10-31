from pos import Pos
from location import Location
# Represents a Car in the traffic simulation
class Car:
    def __init__(self, curr_pos: Pos, on_side: Location, source: Pos, dest: Pos):
        self.curr_pos = curr_pos
        self.on_side = on_side # what side of the intersection the car is on. A car is always moving out of an intersecion

        self.source = source
        self.dest = dest


    def __str__(self):
        return f"Car at {self.curr_pos}, coming from direction {self.on_side}, orginating from{self.source}, and heading to {self.dest}"
    
    # moves a car from it's current position to its new position
    def move(self,dir):
        movement = self.on_side.math_dirs()
        new_postiion = Pos(self.curr_pos + movement[0], self.curr_pos + movement[1])
        self.on_side = dir
        self.curr_pos = new_postiion

    # is the car at it's destination
    def at_destination(self):
        return self.curr_pos == self.dest


        


