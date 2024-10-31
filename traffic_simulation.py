from car import Car
from pos import Pos
from Location import Location
import random
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
        self.cars = self.place_random_cars()
        

    def setup():
        pass

    # place cars randomly on the map
    def place_random_cars(self):
        cars = []
        for _ in range(self.num_of_cars):
            src_x = random.randint(1, self.height-2)
            src_y = random.randint(1, self.width-2)
            dest_x = random.randint(1, self.height-2)
            dest_y = random.randint(1, self.width-2)
            coming_from = Location(random.randint(0, 3))
            car = Car(Pos(src_x, src_y),coming_from, Pos(src_x, src_y), Pos(dest_x,dest_y))
            cars.append(car)
        return cars
            


if __name__ == "__main__":
    ts = TrafficSimulation()






  
   