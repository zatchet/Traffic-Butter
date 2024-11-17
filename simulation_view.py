import pygame
import time
from location import Location
import random 
from typing import List
from intersection import Intersection, StopLight, StopSign
from traffic_simulation import TrafficSimulation

#CONSTANTS
cellSize = 75 # pixels
car_size = 20
black = (0, 0, 0)

white = (255, 255, 255)
green = (0, 128, 0)
red = (255, 0, 0)
fps = 60

   
 # TODO move to run.py (in here for testing purposes)       
def random_intersection_placement(width: int, height: int) -> List[List[Intersection]]:
    matrix = [[None for i in range(width)] for i in range(height)]
    print(matrix, 'matrix creation')
    for y in range(height):
        for x in range(width):
            if y == 0 or x == 0:
                continue
            random_intersection = random.randint(0, 1)
            if random_intersection == 1:
                matrix[y][x] = StopLight()
            else:
                matrix[y][x] = StopSign()
    return matrix 
       
# Represents all information to rendering the game
class GameLoop:
    def __init__(self):
        self.traffic_simulation = TrafficSimulation(matrix=random_intersection_placement(9, 9), stop_light_duration=1.5)
        self.screen_height = cellSize * self.traffic_simulation.height
        self.screen_width = cellSize * self.traffic_simulation.width
        self.car_index = 0
        self.last_move_time = time.time()
        self.move_interval = 1.0

    def drawGrid(self, screen):
        for y in range(0, self.screen_height, cellSize):
            for x in range(0, self.screen_width, cellSize):
                rect = pygame.Rect(x, y, cellSize, cellSize)
                pygame.draw.rect(screen, black, rect, 1)   

    def drawCars(self, screen):
        for i, car in enumerate(self.traffic_simulation.cars):
            x = car.curr_pos.x
            y = car.curr_pos.y
            location = car.on_side
            dir_val_x = location.math_dirs()[0]
            dir_val_y = location.math_dirs()[1]
            rect = pygame.Rect((x*cellSize) + (0 if (dir_val_x >= 0) else -car_size), 
                               (y*cellSize) + (0 if (dir_val_y >= 0) else -car_size), 
                               car_size + (-abs(dir_val_y)*(car_size/2)), 
                               car_size + (-abs(dir_val_x)*(car_size/2)))
            pygame.draw.rect(screen, car.color, rect, 4 if i == self.car_index else 0)
            pygame.draw.circle(screen, car.color,(((x*cellSize) + (dir_val_x*(car_size*1.25))+ ((car_size/4) if dir_val_x == 0 else 0)), 
                                                  ((y*cellSize) + (dir_val_y*(car_size*1.25))+ ((car_size/4) if dir_val_y == 0 else 0))), 
                                                  (car_size/4))

    def draw_intersection_elements(self, screen):
        for y in range(0, len(self.traffic_simulation.matrix)):
            for x in range(0, len(self.traffic_simulation.matrix[0])):
                intersection = self.traffic_simulation.matrix[y][x]
                if type(intersection) == StopLight:
                    pygame.draw.circle(screen, green if not intersection.y_axis_green else red, ((x*cellSize) - 8,(y * cellSize)), 5)
                    pygame.draw.circle(screen, green if not intersection.y_axis_green else red, ((x*cellSize) + 8,(y * cellSize)), 5)
                    pygame.draw.circle(screen, green if intersection.y_axis_green else red, ((x*cellSize),(y * cellSize) - 8), 5)
                    pygame.draw.circle(screen, green if intersection.y_axis_green else red, ((x*cellSize),(y * cellSize) + 8), 5)
                if type(intersection) == StopSign:
                    rect = pygame.Rect((x*cellSize)-4,
                                       (y*cellSize)-4,
                                       10,
                                       10)
                    pygame.draw.rect(screen, red, rect)

    # begins the simuation
    def start(self):
        self.loop_gui()

    def refresh(self, screen):
        screen.fill(white)
        self.draw_city(screen)

    def draw_city(self, screen):
        self.drawGrid(screen)
        self.drawCars(screen)
        self.draw_intersection_elements(screen)
    
    def loop_gui(self):
        pygame.init()
        screen = pygame.display.set_mode((self.screen_height, self.screen_width))
        pygame.display.set_caption("Traffic Simulation")
        self.refresh(screen)

        while True:
            pygame.display.flip()
            self.refresh(screen)
            current_time = time.time()
            # move cars every move_interval seconds
            if current_time - self.last_move_time >= self.move_interval:
                self.traffic_simulation.update_car_positions()
                self.last_move_time = current_time
            
            if self.traffic_simulation.done():
                result = self.traffic_simulation.result()
                pygame.display.flip()
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
            
        print(f"average time to destination: {result} seconds")
        pygame.quit()
        

if __name__ == "__main__":
    gl = GameLoop()
    gl.start()
    