from typing import List
from car import Car
from pos import Pos
from location import Location
import random

car_colors = [(134, 56, 210), (29, 254, 155), (98, 92, 9), (20, 25, 253), (24, 121, 41), (123, 245, 86), (155, 194, 214), (46, 163, 45), (253, 221, 106), (37, 38, 175)]
# Main logic for the Traffic Simulation 
# Pygame should not be in this file
class TrafficSimulation:
    def __init__(self,  matrix: List[List[int]], height: int = 9, width: int = 9, num_of_cars: int = 6, speed_of_cars: float = 3):
        if height < 2 or width < 2 or num_of_cars <= 0 or speed_of_cars <= 0 or len(matrix) != height or len(matrix[0]) != width:
            raise Exception("Invalid input to Traffic Simulation")
        self.height = height
        self.width = width
        self.num_of_cars = num_of_cars
        self.speed_of_cars = speed_of_cars
        self.grid = [[0]*height]*width
        self.cars = self.place_random_cars()
        self.matrix = matrix

    def move_car(self, car_index: int, direction: Location):
        if car_index >= len(self.cars):
            raise Exception("move_car: Invalid index of car")
        car = self.cars[car_index]
        curr_position = car.curr_pos
        direction_math = direction.math_dirs()
        new_x = curr_position.x + direction_math[0]
        new_y = curr_position.y + direction_math[1]
        if not 0 < new_x < len(self.grid[0]) or not 0 < new_y < len(self.grid):
            print("moving car out of bounds")
            return
        new_position = Pos(new_x, new_y)
        car.on_side = direction
        car.curr_pos = new_position 

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
            color = random.choice(car_colors)
            car = Car(Pos(src_x, src_y),coming_from, Pos(src_x, src_y), Pos(dest_x,dest_y), color)
            cars.append(car)
        return cars





#if __name__ == "__main__":
    #ts = TrafficSimulation(matrix=random_intersection_placement(9, 9))






  
   