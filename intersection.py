import random
import threading
from direction import Direction
from constants import *

# represents types of intersections that can exist in the traffic simulation
class Intersection:
    pass

class StopLight(Intersection):
    def __init__(self, duration, y_axis_green):
        self.y_axis_green = y_axis_green
        self.queues = {direction: [] for direction in Direction}
        self.duration = duration

    # every duration seconds, flip the light
    def flip_light(self, ts):
        self.y_axis_green = not self.y_axis_green
        queues_to_be_processed = [queue.copy() for queue in self.queues.values() if len(queue) > 0]
        if len(queues_to_be_processed) > 2:
            raise Exception("Should never be more than 2 queues with cars")
        self.queues = {direction: [] for direction in Direction}
        self.process_queues(ts, queues_to_be_processed)
        threading.Timer(self.duration, self.flip_light, kwargs={'ts': ts}).start()
    
    # release a car from each of the 2 queues every LIGHT_RELEASE_RATE seconds
    def process_queues(self, ts, queues):
        if len(queues) == 0:
            return

        for queue in queues:
            if len(queue) == 0:
                continue
            car_index, next_direction = queue.pop(0)  # Get first car in queue
            left_turn_penalty = 0.5 if next_direction == Direction.left else 0
            threading.Timer(left_turn_penalty, ts.release_car_from_queue, kwargs={'car_index': car_index}).start()
        
        # If there are more cars in either queue, schedule the next one
        if any(len(queue) > 0 for queue in queues):
            threading.Timer(LIGHT_RELEASE_RATE, self.process_queues, kwargs={'ts': ts, 'queues': queues}).start()

    def join(self, car_index, direction, next_direction, ts):
        # if car index in any queue, it cannot re-join this intersection
        for queue in self.queues.values():
            if car_index in queue:
                return
        if direction in [Direction.up, Direction.down] and self.y_axis_green:
            # green light, immediately let the car through
            ts.release_car_from_queue(car_index)
            return
        if direction in [Direction.left, Direction.right] and not self.y_axis_green:
            # green light, immediately let the car through
            ts.release_car_from_queue(car_index)
            return
        # red light, add to proper queue
        self.queues[direction].append((car_index, next_direction))
    
class FourWayStopSign(Intersection):
    def __init__(self):
        self.time_since_last_pass = 0
        self.cars_waiting = 0
        
    def join(self, car_index, direction, next_direction, ts):
        self.cars_waiting += 1
        threading.Timer(STOP_SIGN_RELEASE_RATE*self.cars_waiting, self.release_car, kwargs={'ts': ts, 'car_index': car_index}).start()
    
    def release_car(self, ts, car_index):
        ts.release_car_from_queue(car_index)
        self.cars_waiting -= 1

class TwoWayStopSign(Intersection):
    def __init__(self, y_axis_free):
        self.y_axis_free = y_axis_free
        if self.y_axis_free:
            # maintain two queues, one for each stop sign
            self.queues = {direction: [] for direction in [Direction.left, Direction.right]}
        else:
            # maintain two queues, one for each stop sign
            self.queues = {direction: [] for direction in [Direction.up, Direction.down]}
    
    def join(self, car_index, direction, next_direction, ts):
        if direction in [Direction.up, Direction.down] and self.y_axis_free:
            # no stop, immediately let the car through
            ts.release_car_from_queue(car_index)
            return
        if direction in [Direction.left, Direction.right] and not self.y_axis_free:
            # no stop, immediately let the car through
            ts.release_car_from_queue(car_index)
            return
        # stop sign, add to proper queue
        self.queues[direction].append(car_index)
        cars_in_queue = len(self.queues[direction])
        threading.Timer(STOP_SIGN_RELEASE_RATE*cars_in_queue, 
                        self.release_car, kwargs={'ts': ts, 'car_index': car_index, 'direction': direction, 'next_direction': next_direction}).start()

    def release_car(self, ts, car_index, direction,next_direction):
        left_turn_penalty = 0.5 if next_direction == Direction.left else 0
        threading.Timer(left_turn_penalty, ts.release_car_from_queue, kwargs={'car_index': car_index}).start()
        self.queues[direction].remove(car_index)
