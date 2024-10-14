# Main logic for the Traffic Simulation 
# Pygame should not be in this file
class TrafficSimulation:
    def __init__(self, height: int = 9, width: int = 9, num_of_cars: int = 6, speed_of_cars: float = 3):
        if height < 2 or width < 2 or num_of_cars <= 0 or speed_of_cars <= 0:
            raise Exception("Invalid input to Traffic Simulation")
        self.height = height
        self.width = width
        self.num_of_cars = num_of_cars
        self.speed_of_cars = speed_of_cars
        self.grid = [[0]*height]*width

    def setup():
        pass





  
   