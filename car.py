from typing import Tuple
from pos import Pos
from location import Location
# Represents a Car in the traffic simulation

class Car:
    id = 0
    # id is the index of the car in the traffic simulation's cars list
    def __init__(self, curr_pos: Pos, on_side: Location, source: Pos, dest: Pos, color: Tuple[int]):
        self.id = Car.id
        self.curr_pos = curr_pos
        self.on_side = on_side # what side of the intersection the car is on. A car is always moving out of an intersecion
        self.color = color
        self.source = source
        self.dest = dest
        self.in_queue = False
        self.route = self.generate_route(source, dest)
        self.route_index = 0 # keeps track of where the car is along its route
        Car.id += 1

    def __str__(self):
        return f"Car at {self.curr_pos}, coming from direction {self.on_side}, orginating from{self.source}, and heading to {self.dest}"
    
    # is the car at it's destination
    def at_destination(self):
        return self.curr_pos == self.dest
    
    def get_next_move(self):
        if self.route_index >= len(self.route):
            return None  # Route completed
            
        next_move = self.route[self.route_index]
        return next_move
    
    def generate_route(self, source: Pos, dest: Pos) -> list[Location]:
        return [Location(0), Location(0), Location(0), Location(0), Location(2)]  # Example route
        # for now, just straight line from source to dest
        route = []
        current = source
        
        while current != dest:
            # Determine direction based on relative positions
            dx = dest.x - current.x
            dy = dest.y - current.y
            
            if dx > 0:
                route.append(Location.right)
                current = Pos(current.x + 1, current.y)
            elif dx < 0:
                route.append(Location.left)
                current = Pos(current.x - 1, current.y)
            elif dy > 0:
                route.append(Location.down)
                current = Pos(current.x, current.y + 1)
            elif dy < 0:
                route.append(Location.up)
                current = Pos(current.x, current.y - 1)
        return route