import threading
from typing import List
from car import Car
from pos import Pos
from location import Location
import random
import time
import math
from intersection import StopLight, StopSign

car_colors = [(134, 56, 210), (29, 254, 155), (98, 92, 9), (20, 25, 253), (24, 121, 41), (123, 245, 86), (155, 194, 214), (46, 163, 45), (253, 221, 106), (37, 38, 175)]
# Main logic for the Traffic Simulation 
# Pygame should not be in this file
class TrafficSimulation:
    def __init__(self,  matrix: List[List[int]], stop_light_duration, height: int = 9, width: int = 9, num_of_cars: int = 6, speed_of_cars: float = 3):
        if height < 2 or width < 2 or num_of_cars <= 0 or speed_of_cars <= 0 or len(matrix) != height or len(matrix[0]) != width:
            raise Exception("Invalid input to Traffic Simulation")
        self.height = height
        self.width = width
        self.speed_of_cars = speed_of_cars # this isn't used at the moment
        self.grid = [[0]*height]*width
        self.cars = self.place_random_cars(num_of_cars)
        self.matrix = matrix
        self.stop_light_duration = stop_light_duration
        self.start_time = time.time()
        self.times = [math.inf]*num_of_cars
        self.setup_thread_for_light_toggle()

    def update_car_positions(self):
        for car in self.cars:
            next_move = car.get_next_move()
            if next_move:
                self.move_car(self.cars.index(car), next_move)

    # moves a car from it's current position to its new position, and joins the queue for whatever intersection is at the new position
    def move_car(self, car_index: int, direction: Location):
        if car_index >= len(self.cars):
            raise Exception("move_car: Invalid index of car")
        if (self.cars[car_index].in_queue):
            return print("Can't move car, already in queue for a light")
        car = self.cars[car_index]
        curr_position = car.curr_pos
        direction_math = direction.math_dirs()
        new_x = curr_position.x + direction_math[0]
        new_y = curr_position.y + direction_math[1]
        if not 0 < new_x < len(self.grid[0]) or not 0 < new_y < len(self.grid):
            print("moving car out of bounds")
            return
        intersection = self.matrix[new_y][new_x]
        car.in_queue = True
        intersection.join_queue(car_index, direction, self)
                    

    def move_car_to_next_intersection(self, car_index, direction):
        car = self.cars[car_index]
        curr_position = car.curr_pos
        direction_math = direction.math_dirs()

        car.route_index += 1

        new_x = curr_position.x + direction_math[0]
        new_y = curr_position.y + direction_math[1]

        new_position = Pos(new_x, new_y)
        self.cars[car_index].in_queue = False
        car.on_side = direction
        car.curr_pos = new_position 
        print(f'Car:{car_index} moved from {curr_position} to {new_position}')
        if car.at_destination():
            print('logging time')
            self.times[car_index] = time.time() - self.start_time


    def setup_thread_for_light_toggle(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                if type(self.matrix[i][j]) == StopLight:
                    self.matrix[i][j].flip_light(self)
        threading.Timer(self.stop_light_duration, self.setup_thread_for_light_toggle).start()

    def result(self):
        return sum(self.times) / len(self.times)
    
    def done(self):
        return all(car.at_destination() for car in self.cars)

    # place cars randomly on the map
    def place_random_cars(self, num_of_cars):
        cars = []
        for i in range(2,8):
            src_x = random.randint(1, self.height-2)
            src_y = random.randint(1, self.width-2)
            dest_x = random.randint(1, self.height-2)
            dest_y = random.randint(1, self.width-2)
            coming_from = Location(random.randint(0, 3))
            color = random.choice(car_colors)

            car = Car(Pos(i, 7), coming_from, Pos(src_x, src_y), Pos(i - 1,3), color)
            cars.append(car)
        return cars






    




#if __name__ == "__main__":
    #ts = TrafficSimulation(matrix=random_intersection_placement(9, 9))






  
   