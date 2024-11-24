import threading
import random
from direction import Direction
from constants import *

# does func with kwargs after time seconds
def start_timer(time, func, kwargs):
    timer = threading.Timer(time, func, kwargs=kwargs)
    timer.daemon = True
    timer.start()

# represents types of intersections that can exist in the traffic simulation
class Intersection:
    pass

class StopLight(Intersection):
    def __init__(self, duration_pattern):
        self.y_axis_green = random.choice([True, False])
        self.queues = {direction: [] for direction in Direction}
        self.duration_pattern = duration_pattern  # (y_axis_green seconds, y_axis_red seconds)

    def __repr__(self):
        return f"StopLight({self.duration_pattern})"

    def flip_light(self, ts):
        if ts.done():
            return
        self.y_axis_green = not self.y_axis_green
        queues_to_be_processed = [queue.copy() for queue in self.queues.values() if len(queue) > 0]
        if len(queues_to_be_processed) > 2:
            raise Exception("Should never be more than 2 queues with cars")
        self.queues = {direction: [] for direction in Direction}
        start_timer(LIGHT_RELEASE_RATE, self.process_queues, kwargs={'ts': ts, 'queues': queues_to_be_processed})
        flip_time = self.duration_pattern[0] if self.y_axis_green else self.duration_pattern[1]
        start_timer(flip_time, self.flip_light, kwargs={'ts': ts})
    
    # release a car from each of the 2 queues every LIGHT_RELEASE_RATE seconds
    def process_queues(self, ts, queues):
        if len(queues) == 0:
            return

        for queue in queues:
            if len(queue) == 0:
                continue
            car_index, next_direction = queue.pop(0)  # Get first car in queue
            left_turn_penalty = LEFT_TURN_PENALTY if next_direction == Direction.left else 0
            start_timer(left_turn_penalty, ts.release_car_from_queue, kwargs={'car_index': car_index})
        
        # If there are more cars in either queue, schedule the next one
        if any(len(queue) > 0 for queue in queues):
            timer = threading.Timer(LIGHT_RELEASE_RATE, self.process_queues, kwargs={'ts': ts, 'queues': queues})
            timer.daemon = True
            timer.start()

    def join(self, car_index, direction, next_direction, ts):
        # if car index in any queue, it cannot re-join this intersection
        for queue in self.queues.values():
            if car_index in queue:
                return
        if direction in [Direction.up, Direction.down] and self.y_axis_green:
            # green light, immediately let the car through
            start_timer(MOVEMENT_DELAY, ts.release_car_from_queue, kwargs={'car_index': car_index})
            return
        if direction in [Direction.left, Direction.right] and not self.y_axis_green:
            # green light, immediately let the car through
            start_timer(MOVEMENT_DELAY, ts.release_car_from_queue, kwargs={'car_index': car_index})
            return
        # red light, add to proper queue
        self.queues[direction].append((car_index, next_direction))
    
class FourWayStopSign(Intersection):
    def __init__(self):
        self.time_since_last_pass = 0
        self.cars_waiting = 0

    def __repr__(self):
        return f"FourWayStopSign()"
        
    def join(self, car_index, direction, next_direction, ts):
        self.cars_waiting += 1
        start_timer(STOP_SIGN_RELEASE_RATE*self.cars_waiting, self.release_car, kwargs={'ts': ts, 'car_index': car_index})
    
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

    def __repr__(self):
        return f"TwoWayStopSign({self.y_axis_free})"
    
    def join(self, car_index, direction, next_direction, ts):
        if direction in [Direction.up, Direction.down] and self.y_axis_free:
            # no stop, immediately let the car through
            start_timer(MOVEMENT_DELAY, ts.release_car_from_queue, kwargs={'car_index': car_index})
            return
        if direction in [Direction.left, Direction.right] and not self.y_axis_free:
            # no stop, immediately let the car through
            start_timer(MOVEMENT_DELAY, ts.release_car_from_queue, kwargs={'car_index': car_index})
            return
        # stop sign, add to proper queue
        self.queues[direction].append(car_index)
        cars_in_queue = len(self.queues[direction])
        start_timer(STOP_SIGN_RELEASE_RATE*cars_in_queue, self.release_car, kwargs={'ts': ts, 'car_index': car_index, 'direction': direction, 'next_direction': next_direction})

    def release_car(self, ts, car_index, direction,next_direction):
        left_turn_penalty = LEFT_TURN_PENALTY if next_direction == Direction.left else 0
        start_timer(left_turn_penalty, ts.release_car_from_queue, kwargs={'car_index': car_index})
        self.queues[direction].remove(car_index)
