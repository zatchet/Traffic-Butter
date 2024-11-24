from traffic_simulation import TrafficSimulation
from constants import *
from typing import List
from intersection import Intersection
from traffic_simulation import random_matrix, random_intersection
import threading
import random
from multiprocessing import Pool
import time
from pos import Pos
from intersection import StopLight, FourWayStopSign, TwoWayStopSign
from simulation_view import SimulationView
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

GRID_WIDTH = 6
GRID_HEIGHT = 6

## only one of the following variables should be non-None at a time
# set this variable if we want to have consistent origin-destination pairs across the entire algorithm
ORIGIN_DESTINATION_PAIRS = [(Pos(random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)), 
                             Pos(random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))) for _ in range(50)]
# set this variable if we want to randomize car origin/destinations every simulation
NUM_OF_CARS = None

INITIAL_CANDIDATE_COUNT = 10
SURVIVOR_COUNT = 5 # the top SURVIVOR_COUNT candidates are preserved for the next generation

RUNS_PER_CANDIDATE = 3

MUTATION_RATE_INITIAL = 0.9
MUTATION_DECAY_RATE = 0.9

CONVERGENCE_THRESHOLD = 5 # number of generations without improvement
NUM_RESTARTS = 5

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
    return (candidate, sum(results) / len(results))

def intersection_type_crossover(candidate1: List[List[Intersection]], candidate2: List[List[Intersection]]):
    # takes the traffic lights from candidate1 and everything else from candidate2
    new_candidate = []
    for y in range(len(candidate1)):
        new_candidate.append([])
        for x in range(len(candidate1[0])):
            if isinstance(candidate1[y][x], StopLight):
                new_candidate[y].append(candidate1[y][x])
            else:
                new_candidate[y].append(candidate2[y][x])
    return new_candidate

def checkerboard_crossover(candidate1: List[List[Intersection]], candidate2: List[List[Intersection]]):
    # builds a new candidate by alternating between the two parents
    new_candidate = []
    for y in range(len(candidate1)):
        new_candidate.append([])
        for x in range(len(candidate1[0])):
            if (y + x) % 2 == 0:
                new_candidate[y].append(candidate1[y][x])
            else:
                new_candidate[y].append(candidate2[y][x])
    return new_candidate

def mutate(candidate: List[List[Intersection]]):
    mutated_candidate = candidate.copy()
    # randomly mutate one intersection
    y = random.randint(0, len(candidate) - 1)
    x = random.randint(0, len(candidate[0]) - 1)
    intersection = candidate[y][x]
    
    if random.random() < 0.4 or isinstance(intersection, FourWayStopSign):
        # change intersection type
        mutated_candidate[y][x] = random_intersection()
    else:
        # tweak property of intersection
        if isinstance(intersection, StopLight):
            if random.random() < 0.5:
                new_duration_pattern = (intersection.duration_pattern[0] + random.choice([-1*SCALE_FACTOR, 1*SCALE_FACTOR]), intersection.duration_pattern[1])
            else:
                new_duration_pattern = (intersection.duration_pattern[0], intersection.duration_pattern[1] + random.choice([-1*SCALE_FACTOR, 1*SCALE_FACTOR]))
            mutated_candidate[y][x] = StopLight(new_duration_pattern)
        elif isinstance(intersection, TwoWayStopSign):
            new_y_axis_free = not intersection.y_axis_free
            mutated_candidate[y][x] = TwoWayStopSign(new_y_axis_free)
    return mutated_candidate

def crossover(candidate1: List[List[Intersection]], candidate2: List[List[Intersection]]):
    if random.random() < 0.5:
        return checkerboard_crossover(candidate1, candidate2)
    else:
        return intersection_type_crossover(candidate1, candidate2)

def create_new_candidates(survivors: List[List[Intersection]], mutation_rate: float):
    results = []
    for candidate in survivors:
        if random.random() < mutation_rate:
            print("mutating")
            new_candidate = mutate(candidate)
        else:
            print("crossover")
            other_candidate = random.choice([c for c in survivors if c != candidate])
            new_candidate = crossover(candidate, other_candidate)
        results.append(new_candidate)
    if random.random() < 0.1:
        # spawn in a new random candidate to keep population diverse
        results.append(random_matrix(GRID_WIDTH, GRID_HEIGHT))
    return results

def collect_results(candidates):
    # Run candidates in parallel
    with Pool(len(candidates)) as p:
        return p.map(run_simulations_on, candidates)

def genetic_algorithm():
    # start with random candidates
    print("Starting genetic algorithm")
    running_best = (None, float('inf'))
    for i in range(NUM_RESTARTS):
        candidates = [random_matrix(GRID_WIDTH, GRID_HEIGHT) for _ in range(INITIAL_CANDIDATE_COUNT)]
        mutation_rate = MUTATION_RATE_INITIAL
        generations_without_improvement = 0
        while True:
            print(f'Running simulations on new generation with mutation rate {mutation_rate}, restart {i}, current best {running_best[1]}')
            results = collect_results(candidates)
            # print([result for candidate, result in results])
            sorted_results = sorted(results, key=lambda x: x[1])    
            survivors = [candidate for candidate, score in sorted_results[:SURVIVOR_COUNT]]
            best_from_this_generation = sorted_results[0]
            if best_from_this_generation[1] < running_best[1]:
                print(f"New best result: {best_from_this_generation[1]}")
                running_best = best_from_this_generation
                generations_without_improvement = 0
            else:
                generations_without_improvement += 1
            if generations_without_improvement >= CONVERGENCE_THRESHOLD:
                print(f"Converged, restarting from scratch")
                break
            new_candidates = create_new_candidates(survivors, mutation_rate)
            mutation_rate *= MUTATION_DECAY_RATE
            candidates = survivors + new_candidates
    return running_best

def draw_solution(solution: List[List[Intersection]]):
    view = SimulationView(TrafficSimulation(matrix=solution, num_of_cars=200), draw_cars=False)
    view.start()

if __name__ == '__main__':
    optimal_result = genetic_algorithm()
    print(f"Optimal result: {optimal_result}")
    draw_solution(optimal_result[0])
