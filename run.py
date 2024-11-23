from traffic_simulation import TrafficSimulation
from constants import *
from typing import List
from intersection import Intersection
from traffic_simulation import random_intersection_placement
import threading
import random
from multiprocessing import Pool
import time
from functools import partial

def stop_all_threads():
    for thread in threading.enumerate():
        if thread != threading.current_thread():
            thread.join()

def run_simulations_on(candidate: List[List[Intersection]], num_of_cars: int, runs_per_candidate: int):
    results = []
    for _ in range(runs_per_candidate):
        #print(f"Running simulation {i}")
        ts = TrafficSimulation(num_of_cars=num_of_cars, matrix=candidate)
        result = ts.run()
        results.append(result)
        stop_all_threads()
    return (candidate, sum(results) / len(results))

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

def collect_results(candidates, num_of_cars, runs_per_candidate):
    # Prepare arguments for each candidate
    func = partial(run_simulations_on, num_of_cars=num_of_cars, runs_per_candidate=runs_per_candidate)
    # Run candidates in parallel
    with Pool(len(candidates)) as p:
        return p.map(func, candidates)

def genetic_algorithm(width: int, height: int, num_of_cars: int, candidate_count: int, runs_per_candidate: int):
    # start with random candidates
    candidates = [random_intersection_placement(width, height) for _ in range(candidate_count)]
    while True:
        results = collect_results(candidates, num_of_cars, runs_per_candidate)
        sorted_results = sorted(results, key=lambda x: x[1])    
        best_half = [candidate for candidate, score in sorted_results[:len(candidates)//2]]
        new_candidates = create_new_candidates(best_half, candidate_count)
        candidates = best_half + new_candidates

if __name__ == '__main__':
    start_time = time.time()
    print(POSSIBLE_LIGHT_DURATIONS)
    genetic_algorithm(width=3, height=3, num_of_cars=3, candidate_count=4, runs_per_candidate=2)
