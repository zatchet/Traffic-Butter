from traffic_simulation import TrafficSimulation
from constants import *
from typing import List
from intersection import Intersection
from traffic_simulation import random_intersection_placement
import threading
import random

def stop_all_threads():
    for thread in threading.enumerate():
        if thread != threading.current_thread():
            thread.join()

def run_simulations_on(candidate: List[List[Intersection]], num_of_cars: int, runs_per_candidate: int):
    results = []
    for _ in range(runs_per_candidate):
        ts = TrafficSimulation(num_of_cars=num_of_cars, matrix=candidate)
        result = ts.run()
        results.append(result)
        stop_all_threads()
    return sum(results) / len(results)

def mutate(candidate: List[List[Intersection]]):
    # not implemented
    return candidate

def crossover(candidate1: List[List[Intersection]], candidate2: List[List[Intersection]]):
    # not implemented
    return candidate1

def create_new_candidates(best_half: List[List[Intersection]], candidate_count: int):
    # results should be of length candidate_count - len(best_half)
    # not implemented
    results = []
    for _ in range(candidate_count - len(best_half)):
        results.append(random.choice(best_half))
    return results

def genetic_algorithm(width: int, height: int, num_of_cars: int, candidate_count: int, runs_per_candidate: int):
    # start with random candidates
    candidates = [random_intersection_placement(width, height) for _ in range(candidate_count)]
    while True:
        # should check out the multiprocessing package to run candidates in parallel
        results = [(candidate, run_simulations_on(candidate, num_of_cars, runs_per_candidate)) for candidate in candidates]
        sorted_results = sorted(results, key=lambda x: x[1])    
        best_half = [candidate for candidate, score in sorted_results[:len(candidates)//2]]
        new_candidates = create_new_candidates(best_half, candidate_count)
        candidates = best_half + new_candidates

if __name__ == '__main__':
    print(POSSIBLE_LIGHT_DURATIONS)
    genetic_algorithm(width=3, height=3, num_of_cars=3, candidate_count=4, runs_per_candidate=2)
