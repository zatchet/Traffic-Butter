from enum import Enum

import time
import random
import threading
from location import Location
stop_sign_delay = 2
# represents types of intersections that can exist in the traffic simulation
class Intersection:
    def canPass() -> bool:
        return
class StopLight(Intersection):
    
    def __init__(self):
        self.y_axis_green = bool(random.randint(0,1))
        self.queue = [] # (index of car, direction)

    def flip_light(self, ts):
        self.y_axis_green = not self.y_axis_green
        for car_index, direction in self.queue:
            ts.move_car_to_next_intersection(car_index, direction)
        self.queue = []

        

    def join_queue(self, car_index, direction, ts):
        if (car_index, direction) in self.queue:
            return
        if (self.y_axis_green) and (direction == Location.left or direction == Location.right):
            self.queue.append((car_index,direction))
            print('attempting to move at a red light')
            return
        if not self.y_axis_green and (direction == Location.up or direction == Location.down):
            self.queue.append((car_index,direction))
            print('attempting to move at a red light')
            return
        ts.move_car_to_next_intersection(car_index, direction)
        
       
    
class StopSign(Intersection):
    def __init__(self):
        self.time_since_last_pass = 0
        self.queue = []
        

    def join_queue(self, car_index, direction, ts):
        if car_index in self.queue:
            print('car already at intersection')
            return
        
        if self.time_since_last_pass + stop_sign_delay < time.time():
            ts.move_car_to_next_intersection(car_index, direction)
            self.time_since_last_pass = time.time()
        else:
            self.queue.append(car_index)
            move_after = max(0, stop_sign_delay - (time.time()- self.time_since_last_pass))
            print(move_after)
            threading.Timer(move_after, self.move_car_thread, kwargs={'car_index': car_index, 'direction': direction, 'ts': ts}).start()

    def move_car_thread(self, car_index, direction, ts):
        self.queue.remove(car_index)
        ts.move_car_to_next_intersection(car_index, direction)

        

