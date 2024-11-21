from enum import Enum

import time
import random
import threading
from direction import Direction
from constants import *

# represents types of intersections that can exist in the traffic simulation
class Intersection:
    pass

class StopLight(Intersection):
    def __init__(self, duration):
        self.y_axis_green = bool(random.randint(0,1))
        self.queue = [] # (index of car, direction)
        self.duration = duration
        self.release_delay = 1

    def flip_light(self, ts):
        self.y_axis_green = not self.y_axis_green
        if len(self.queue) > 0:
            queue_copy = self.queue.copy()
            self.queue = []
            self.process_queue(ts, queue_copy)
        threading.Timer(self.duration, self.flip_light, kwargs={'ts': ts}).start()
    
    def process_queue(self, ts, queue_copy):
        car_index, direction = queue_copy.pop(0)  # Get first car in queue
        ts.release_car_from_queue(car_index, direction)
        
        # If there are more cars in queue, schedule the next one
        if len(queue_copy) > 0:
            threading.Timer(LIGHT_RELEASE_RATE, self.process_queue, kwargs={'ts': ts, 'queue_copy': queue_copy}).start()

    def join(self, car_index, direction, ts):
        if (car_index, direction) in self.queue:
            return
        if (self.y_axis_green) and (direction == Direction.left or direction == Direction.right):
            self.queue.append((car_index,direction))
            # print('attempting to move at a red light')
            return
        if not self.y_axis_green and (direction == Direction.up or direction == Direction.down):
            self.queue.append((car_index,direction))
            # print('attempting to move at a red light')
            return
        ts.release_car_from_queue(car_index, direction)
    
class StopSign(Intersection):
    def __init__(self):
        self.time_since_last_pass = 0
        self.queue = []
        
    def join(self, car_index, direction, ts):
        if car_index in self.queue:
            # print('car already at intersection')
            return
        
        if self.time_since_last_pass + STOP_SIGN_DELAY < time.time():
            ts.release_car_from_queue(car_index, direction)
            self.time_since_last_pass = time.time()
        else:
            self.queue.append(car_index)
            move_after = max(0, STOP_SIGN_DELAY - (time.time()- self.time_since_last_pass))
            threading.Timer(move_after, self.move_car_thread, kwargs={'car_index': car_index, 'direction': direction, 'ts': ts}).start()

    def move_car_thread(self, car_index, direction, ts):
        self.queue.remove(car_index)
        ts.release_car_from_queue(car_index, direction)