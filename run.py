from traffic_simulation import TrafficSimulation
from constants import *
from typing import List
from intersection import Intersection
from traffic_simulation import random_matrix, random_intersection
import threading
import random
from multiprocessing import Pool
from pos import Pos
from intersection import StopLight, FourWayStopSign, TwoWayStopSign
from simulation_view import SimulationView
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

GUI = True

GRID_WIDTH = 5
GRID_HEIGHT = 5

## only one of the following variables should be non-None at a time
# set this variable if we want to have consistent origin-destination pairs across the entire algorithm
ORIGIN_DESTINATION_PAIRS = [(Pos(0, 0), Pos(GRID_WIDTH - 1, GRID_HEIGHT - 1)), 
                            (Pos(0, 0), Pos(GRID_WIDTH - 1, 0)),
                            (Pos(0, 0), Pos(0, GRID_HEIGHT - 1)),
                            (Pos(GRID_WIDTH - 1, GRID_HEIGHT - 1), Pos(GRID_WIDTH - 1, 0)),
                            (Pos(GRID_WIDTH - 1, GRID_HEIGHT - 1), Pos(0, GRID_HEIGHT - 1)),
                            (Pos(GRID_WIDTH - 1, GRID_HEIGHT - 1), Pos(0, 0)),
                            (Pos(GRID_WIDTH - 1, 0), Pos(GRID_WIDTH - 1, GRID_HEIGHT - 1)),
                            (Pos(GRID_WIDTH - 1, 0), Pos(0, GRID_HEIGHT - 1)),
                            (Pos(GRID_WIDTH - 1, 0), Pos(0, 0)),
                            (Pos(0, GRID_HEIGHT - 1), Pos(GRID_WIDTH - 1, GRID_HEIGHT - 1)),
                            (Pos(0, GRID_HEIGHT - 1), Pos(GRID_WIDTH - 1, 0)),
                            (Pos(0, GRID_HEIGHT - 1), Pos(0, 0))]*4
                            
# set this variable if we want to randomize car origin/destinations every simulation
NUM_OF_CARS = None

POPULATION_SIZE = 20
SURVIVOR_COUNT = POPULATION_SIZE // 2 # the top half of candidates are preserved for the next generation

RUNS_PER_CANDIDATE = 1

MUTATION_RATE_INITIAL = 0.9
MUTATION_DECAY_RATE = 0.9

CONVERGENCE_THRESHOLD = 6 # number of generations without improvement in order to declare a local optimum

NUM_RESTARTS = 3

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
        if GUI:
            result = SimulationView(ts, draw_cars=True).start()
        else:
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

def alternating_row_crossover(candidate1: List[List[Intersection]], candidate2: List[List[Intersection]]):
    # builds a new candidate by alternating between the two parents row by row
    new_candidate = []
    for y in range(len(candidate1)):
        if y % 2 == 0:
            new_candidate.append(candidate1[y])
        else:
            new_candidate.append(candidate2[y])
    return new_candidate

def checkerboard_crossover(candidate1: List[List[Intersection]], candidate2: List[List[Intersection]]):
    # builds a new candidate by alternating between the two parents every cell
    new_candidate = []
    for y in range(len(candidate1)):
        new_candidate.append([])
        for x in range(len(candidate1[0])):
            if (y + x) % 2 == 0:
                new_candidate[y].append(candidate1[y][x])
            else:
                new_candidate[y].append(candidate2[y][x])
    return new_candidate

def subsection_crossover(candidate1: List[List[Intersection]], candidate2: List[List[Intersection]]):
    # takes the middle subsection of candidate 1 and the rest from candidate 2
    width = len(candidate1[0])
    height = len(candidate1)
    
    # Calculate middle section boundaries (approximately 50% of grid)
    # Special case for size 3: middle section should be just the center cell
    # For other odd numbers like 7, we want about 40% of the grid
    # For even numbers, we want about half
    def get_start_pos(size):
        if size == 3:
            return 1
        return (size - 1) // 3 if size % 2 == 1 else size // 4
    
    mid_width_start = get_start_pos(width)
    mid_width_end = width - mid_width_start
    mid_height_start = get_start_pos(height)
    mid_height_end = height - mid_height_start
    
    new_candidate = []
    for y in range(height):
        new_candidate.append([])
        for x in range(width):
            if mid_width_start <= x < mid_width_end and mid_height_start <= y < mid_height_end:
                new_candidate[y].append(candidate1[y][x])
            else:
                new_candidate[y].append(candidate2[y][x])
    return new_candidate
    
def crossover(candidate1: List[List[Intersection]], candidate2: List[List[Intersection]]):
    random_number = random.random()
    if random_number < 0.25:
        return checkerboard_crossover(candidate1, candidate2)
    elif random_number < 0.5:
        return alternating_row_crossover(candidate1, candidate2)
    else:
        return subsection_crossover(candidate1, candidate2)

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
                new_duration_pattern = (random.choice(POSSIBLE_LIGHT_DURATIONS), intersection.duration_pattern[1])
            else:
                new_duration_pattern = (intersection.duration_pattern[0], random.choice(POSSIBLE_LIGHT_DURATIONS))
            mutated_candidate[y][x] = StopLight(new_duration_pattern)
        elif isinstance(intersection, TwoWayStopSign):
            new_y_axis_free = not intersection.y_axis_free
            mutated_candidate[y][x] = TwoWayStopSign(new_y_axis_free)
    return mutated_candidate

def get_new_candidates(survivors: List[List[Intersection]], mutation_rate: float):
    new_candidates = []
    for candidate in survivors:
        other_candidate = random.choice([c for c in survivors if c != candidate])
        new_candidates.append(crossover(candidate, other_candidate))
    result = survivors + new_candidates

    # apply mutations
    for i in range(len(result)):
        if random.random() < mutation_rate:
            result[i] = mutate(result[i])
    
    if random.random() < 0.1:
        # spawn in a new random candidate to keep population diverse
        result.append(random_matrix(GRID_WIDTH, GRID_HEIGHT))

    return result

def collect_results(candidates):
    # Run candidates in parallel
    with Pool(len(candidates)) as p:
        return p.map(run_simulations_on, candidates)

def genetic_algorithm():
    print("Starting genetic algorithm")
    best_overall = (None, float('inf'))
    for i in range(NUM_RESTARTS):
        # start with random candidates
        candidates = [random_matrix(GRID_WIDTH, GRID_HEIGHT) for _ in range(POPULATION_SIZE)]
        mutation_rate = MUTATION_RATE_INITIAL
        generation_count = 0
        generations_without_improvement = 0
        best_from_this_restart = (None, float('inf'))
        while generations_without_improvement < CONVERGENCE_THRESHOLD:
            print(f'Running simulations on generation {generation_count} of restart {i} with mutation rate {mutation_rate}. Best from this restart {best_from_this_restart[1]}, best overall {best_overall[1]}')
            results = collect_results(candidates)
            # print([result for candidate, result in results])
            sorted_results = sorted(results, key=lambda x: x[1])    
            survivors = [candidate for candidate, score in sorted_results[:SURVIVOR_COUNT]]
            best_from_this_generation = sorted_results[0]
            if best_from_this_generation[1] < best_from_this_restart[1]:
                print(f'New best result from this restart: {best_from_this_generation[1]}')
                best_from_this_restart = best_from_this_generation
                generations_without_improvement = 0
            else:
                generations_without_improvement += 1
            candidates = get_new_candidates(survivors, mutation_rate)
            mutation_rate *= MUTATION_DECAY_RATE
            generation_count += 1
        if best_from_this_restart[1] < best_overall[1]:
            print(f'New best result overall: {best_from_this_restart[1]}')
            best_overall = best_from_this_restart
    return best_overall

def draw_solution(solution: List[List[Intersection]]):
    view = SimulationView(TrafficSimulation(matrix=solution, num_of_cars=1000), draw_cars=False)
    view.start()

if __name__ == '__main__':
    optimal_result = genetic_algorithm()
    print(f"Optimal result: {optimal_result}")
    draw_solution(optimal_result[0])