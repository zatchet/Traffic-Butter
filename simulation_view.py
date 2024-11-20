import pygame
import time
import random 
from typing import List
from intersection import Intersection, StopLight, StopSign
from traffic_simulation import TrafficSimulation
from constants import *
       
# Represents all information to rendering the game
class GameLoop:
    def __init__(self):
        self.traffic_simulation = TrafficSimulation(num_of_cars=30)
        self.screen_height = CELL_SIZE * self.traffic_simulation.height
        self.screen_width = CELL_SIZE * self.traffic_simulation.width
        self.car_index = 0

    def drawGrid(self, screen):
        for y in range(0, self.screen_height, CELL_SIZE):
            for x in range(0, self.screen_width, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, BLACK, rect, 1)   

    def drawCars(self, screen):
        for car in self.traffic_simulation.cars:
            x = car.curr_pos.x
            y = car.curr_pos.y
            location = car.on_side
            dir_val_x = location.math_dirs()[0]
            dir_val_y = location.math_dirs()[1]
            rect = pygame.Rect((x*CELL_SIZE) + (0 if (dir_val_x >= 0) else -CAR_SIZE), 
                               (y*CELL_SIZE) + (0 if (dir_val_y >= 0) else -CAR_SIZE), 
                               CAR_SIZE + (-abs(dir_val_y)*(CAR_SIZE/2)), 
                               CAR_SIZE + (-abs(dir_val_x)*(CAR_SIZE/2)))
            pygame.draw.rect(screen, car.color, rect, 0)
            pygame.draw.circle(screen, car.color,(((x*CELL_SIZE) + (dir_val_x*(CAR_SIZE*1.25))+ ((CAR_SIZE/4) if dir_val_x == 0 else 0)), 
                                                  ((y*CELL_SIZE) + (dir_val_y*(CAR_SIZE*1.25))+ ((CAR_SIZE/4) if dir_val_y == 0 else 0))), 
                                                  (CAR_SIZE/4))

    def draw_intersection_elements(self, screen):
        for y in range(0, len(self.traffic_simulation.matrix)):
            for x in range(0, len(self.traffic_simulation.matrix[0])):
                intersection = self.traffic_simulation.matrix[y][x]
                if type(intersection) == StopLight:
                    pygame.draw.circle(screen, GREEN if not intersection.y_axis_green else RED, ((x*CELL_SIZE) - 8,(y * CELL_SIZE)), 5)
                    pygame.draw.circle(screen, GREEN if not intersection.y_axis_green else RED, ((x*CELL_SIZE) + 8,(y * CELL_SIZE)), 5)
                    pygame.draw.circle(screen, GREEN if intersection.y_axis_green else RED, ((x*CELL_SIZE),(y * CELL_SIZE) - 8), 5)
                    pygame.draw.circle(screen, GREEN if intersection.y_axis_green else RED, ((x*CELL_SIZE),(y * CELL_SIZE) + 8), 5)
                if type(intersection) == StopSign:
                    rect = pygame.Rect((x*CELL_SIZE)-4,
                                       (y*CELL_SIZE)-4,
                                       10,
                                       10)
                    pygame.draw.rect(screen, RED, rect)

    # begins the simuation
    def start(self):
        self.loop_gui()

    def refresh(self, screen):
        screen.fill(WHITE)
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

        last_move_time = time.time()

        while True:
            pygame.display.flip()
            self.refresh(screen)
            current_time = time.time()
            # move cars every move_interval seconds
            if current_time - last_move_time >= MOVE_INTERVAL:
                self.traffic_simulation.update_car_positions()
                last_move_time = current_time
            
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
    