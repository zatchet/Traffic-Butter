from enum import Enum

# represents one of the four directions on a map
# this location represents where the car is coming from in the intersection. The car is arriving at the intersection from the left side for example
class Location(Enum):
    up = 0
    down = 1
    left = 2
    right = 3
    
    # returns a tuple of (x, y)
    def math_dirs(self):
        match self:
            case self.up:
                return (0,-1)
            case self.down:
                return (0, 1)
            case self.left:
                return (-1, 0)
            case self.right:
                return (1, 0)


