from typing import List
from car import Car
from pos import Pos
from direction import Direction
import random
import time
import math
from intersection import StopLight, Intersection, TwoWayStopSign, FourWayStopSign
from routefinder import RouteFinder
from constants import *

def random_intersection_placement(width: int, height: int) -> List[List[Intersection]]:
    matrix = [[None for _ in range(width)] for _ in range(height)]
    for y in range(1, height):
        for x in range(1, width):
            random_intersection = random.choice([0, 1, 2])
            if random_intersection == 0:
                matrix[y][x] = StopLight(duration = random.choice([5,10]))
            elif random_intersection == 1:
                matrix[y][x] = FourWayStopSign()
            elif random_intersection == 2:
                matrix[y][x] = TwoWayStopSign(y_axis_free=random.choice([True, False]))
    return matrix 

# Main logic for the Traffic Simulation 
# Pygame should not be in this file
class TrafficSimulation:
    def __init__(self, num_of_cars, matrix: List[List[Intersection]] = random_intersection_placement(10, 10)):
        self.height = len(matrix)
        self.width = len(matrix[0])
        if self.height < 2 or self.width < 2 or num_of_cars <= 0:
            raise Exception("Invalid input to Traffic Simulation")
        self.matrix = matrix
        self.cars = self.initialize_cars(num_of_cars)
        self.start_time = time.time()
        self.times = [math.inf]*num_of_cars
        self.setup_light_timers()

    # moves all cars which are currently free to move
    def update_car_positions(self):
        cars_to_be_updated = [car for car in self.cars if not car.in_queue and not car.finished]
        for car in cars_to_be_updated:
            next_move = car.get_next_move()
            if next_move:
                self.move_car(car.id, next_move)

    # moves a car from it's current position to its new position, and joins the queue for whatever intersection is at the new position
    def move_car(self, car_index: int, direction: Direction):
        car = self.cars[car_index]
        if car_index >= len(self.cars):
            raise Exception("move_car: Invalid index of car") 
        curr_position = car.curr_pos
        direction_math = direction.math_dirs()
        new_x = curr_position.x + direction_math[0]
        new_y = curr_position.y + direction_math[1]
        car.curr_pos = Pos(new_x, new_y)
        car.on_side = direction

        if car.at_destination():
            car.color = 'black'
            car.finished = True
            self.times[car_index] = time.time() - self.start_time
            return
        
        if not (0 < new_x < self.width and 0 < new_y < self.height):
            # print("moving car out of bounds")
            return
        
        car.in_queue = True
        intersection = self.matrix[new_y][new_x]

        next_direction = car.route[car.route_index+1] if car.route_index+1 < len(car.route) else None
        intersection.join(car_index, direction, next_direction, self)

    def release_car_from_queue(self, car_index):
        car = self.cars[car_index]
        car.route_index += 1
        car.in_queue = False

    def setup_light_timers(self):
        # Initialize threads for all intersections
        for y in range(1, self.height):
            for x in range(1, self.width):
                intersection = self.matrix[y][x]
                if isinstance(intersection, StopLight):
                    intersection.flip_light(self)

    def result(self):
        filtered_times = [time for time in self.times if time != math.inf]
        return sum(filtered_times) / len(filtered_times)
    
    def done(self):
        return all(car.finished for car in self.cars)

    # place cars randomly on the map
    def initialize_cars(self, num_of_cars):
        cars = []
        for _ in range(num_of_cars):
            source = Pos(random.randint(1, self.width-1), random.randint(1, self.height-1))
            destination = Pos(random.randint(1, self.width-1), random.randint(1, self.height-1))
            color = random.choice(CAR_COLORS)
            route = RouteFinder().generate_route(source, destination, self.matrix)
            initial_direction = route[0] if len(route) > 0 else Direction.up
            car = Car(initial_direction, source, destination, color, route)
            cars.append(car)

        # manual routes for debugging
        # route = RouteFinder().generate_route(Pos(4,8), Pos(4,8), self.matrix)
        # c1 = Car(Direction(0), Pos(4,6), Pos(4,6), 'red', route)
        # c2 = Car(Direction(0), Pos(4,7), Pos(4,2), 'blue', [Direction.up]*5)
        # c3 = Car(Direction(0), Pos(4,7), Pos(4,2), 'green', [Direction.up]*5)
        # c4 = Car(Direction(0), Pos(4,7), Pos(4,2), 'yellow', [Direction.up]*5)
        # c5 = Car(Direction(0), Pos(4,7), Pos(4,2), 'blue', [Direction.up]*5)
        # c6 = Car(Direction(0), Pos(4,7), Pos(4,2), 'green', [Direction.up]*5)
        # cars = [c2, c3, c4, c5, c6]
        # print('route', c1.route)

        return cars






  
   