from traffic_simulation import TrafficSimulation
from constants import *
from typing import List
from intersection import Intersection
from traffic_simulation import random_intersection_placement
import threading
import random
from multiprocessing import Pool
import time
from pos import Pos

## only one of the following variables should be non-None at a time
# set this variable if we want to have consistent origin-destination pairs across the entire algorithm
ORIGIN_DESTINATION_PAIRS = [(Pos(0, 0), Pos(5, 5))]
# set this variable if we want to randomize car origin/destinations every simulation
NUM_OF_CARS = None

GRID_WIDTH = 6
GRID_HEIGHT = 6
CANDIDATE_COUNT = 10
RUNS_PER_CANDIDATE = 4

def stop_all_threads():
    for thread in threading.enumerate():
        if thread != threading.current_thread():
            thread.join()

def run_simulations_on(candidate: List[List[Intersection]]):
    results = []
    for _ in range(RUNS_PER_CANDIDATE):
        if ORIGIN_DESTINATION_PAIRS:
            ts = TrafficSimulation(matrix=candidate, origin_destination_pairs=ORIGIN_DESTINATION_PAIRS)
        elif NUM_OF_CARS:
            ts = TrafficSimulation(matrix=candidate, num_of_cars=NUM_OF_CARS)
        result = ts.run()
        results.append(result)
        stop_all_threads()
    print(results)
    return (candidate, sum(results) / len(results))

def mutate(candidate: List[List[Intersection]]):
    # not implemented
    return candidate

def crossover(candidate1: List[List[Intersection]], candidate2: List[List[Intersection]]):
    # not implemented
    return candidate1

def create_new_candidates(best_half: List[List[Intersection]], candidate_count: int):
    # result should be of length candidate_count - len(best_half)
    # not implemented
    results = []
    for _ in range(candidate_count - len(best_half)):
        results.append(random.choice(best_half))
    return results

def collect_results(candidates):
    # Run candidates in parallel
    with Pool(len(candidates)) as p:
        return p.map(run_simulations_on, candidates)

def genetic_algorithm():
    # start with random candidates
    candidates = [random_intersection_placement(GRID_WIDTH, GRID_HEIGHT) for _ in range(CANDIDATE_COUNT)]
    while True:
        results = collect_results(candidates)
        # print([result for candidate, result in results])
        sorted_results = sorted(results, key=lambda x: x[1])    
        best_half = [candidate for candidate, score in sorted_results[:len(candidates)//2]]
        new_candidates = create_new_candidates(best_half, CANDIDATE_COUNT)
        candidates = best_half + new_candidates

if __name__ == '__main__':
    start_time = time.time()
    genetic_algorithm()