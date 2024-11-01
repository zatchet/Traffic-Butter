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
        self.speed_of_cars = speed_of_cars
        self.grid = [[0]*height]*width
        self.cars = self.place_random_cars(num_of_cars)
        self.matrix = matrix
        self.stop_light_duration = stop_light_duration
        self.start_time = time.time()
        self.times = [math.inf]*num_of_cars

        self.setup_thread_for_light_toggle()

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
        intersection = self.matrix[curr_position.y][curr_position.x]
        if type(intersection) == StopLight:
            if (intersection.y_axis_green) and (direction == Location.left or direction == Location.right):
                print('attempting to move at a red light')
                return
            if not intersection.y_axis_green and (direction == Location.up or direction == Location.down):
                print('attempting to move at a red light')
                return
            self.move_car_to_next_intersection(car_index, direction)
        else:
            intersection.join_queue(car_index, direction, self)
                    

    def move_car_to_next_intersection(self, car_index, direction):
        car = self.cars[car_index]
        curr_position = car.curr_pos
        direction_math = direction.math_dirs()
        new_x = curr_position.x + direction_math[0]
        new_y = curr_position.y + direction_math[1]

        new_position = Pos(new_x, new_y)
        car.on_side = direction
        car.curr_pos = new_position 
        print(f'Car:{car_index} moved from {curr_position} to {new_position}')



    def setup_thread_for_light_toggle(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                if type(self.matrix[i][j]) == StopLight:
                    self.matrix[i][j].flip_light()
        threading.Timer(self.stop_light_duration, self.setup_thread_for_light_toggle).start()

    def car_at_destination(self, index):
        car = self.cars[index]
        if car.curr_pos == car.dest:
            end_time = time.time()
            time_to_dest = end_time - self.start_time
            self.times[index] = time_to_dest

    def result(self):
        return math.avg(self.times)
    
    def done(self):
        return all(not math.inf == i for i in self.times)


    # place cars randomly on the map
    def place_random_cars(self, num_of_cars):
        cars = []
        for _ in range(num_of_cars):
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






  
   