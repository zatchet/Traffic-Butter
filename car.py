from direction import Direction
# Represents a Car in the traffic simulation
class Car:
    def __init__(self, y: int, x: int, coming_from: Direction):
        self.y = y
        self.x = x
        self.coming_from = coming_from
    
    # moves a car from it's current position to its new position
    def move_to(x, y):
        pass