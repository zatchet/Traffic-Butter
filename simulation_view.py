import pygame
import time
from location import Location
import random 
from typing import List
from intersection import Intersection, StopLight, StopSign
from traffic_simulation import TrafficSimulation

#CONSTANTS
cellSize = 50 # pixels
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
    print(matrix)
    print("")
    return matrix 
       
# Represents all information to rendering the game
class GameLoop:
    def __init__(self):
        self.traffic_simulation = TrafficSimulation(matrix=random_intersection_placement(9, 9), stop_light_duration=1.5)
        self.screen_height = cellSize * self.traffic_simulation.height
        self.screen_width = cellSize * self.traffic_simulation.width
        self.car_index = 0

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
            rect = pygame.Rect((x*cellSize) + (0 if (dir_val_x >= 0) else -20), (y*cellSize) + (0 if (dir_val_y >= 0) else -20), 20 + (-abs(dir_val_y)*10) , 20 + (-abs(dir_val_x)*10))
            pygame.draw.rect(screen, car.color, rect, 4 if i == self.car_index else 10)

    def draw_intersection_elements(self, screen):
        for y in range(0, len(self.traffic_simulation.matrix)):
            for x in range(0, len(self.traffic_simulation.matrix[0])):
                intersection = self.traffic_simulation.matrix[y][x]
                if type(intersection) == StopLight:
                    pygame.draw.circle(screen, green if not intersection.y_axis_green else red, ((x*cellSize) - 5,(y * cellSize)), 4)
                    pygame.draw.circle(screen, green if not intersection.y_axis_green else red, ((x*cellSize) + 5,(y * cellSize)), 4)
                    pygame.draw.circle(screen, green if intersection.y_axis_green else red, ((x*cellSize),(y * cellSize) - 5), 4)
                    pygame.draw.circle(screen, green if intersection.y_axis_green else red, ((x*cellSize),(y * cellSize) + 5), 4)
                if type(intersection) == StopSign:
                    rect = pygame.Rect((x*cellSize)-4,(y*cellSize)-4,8,8)
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
        clock = pygame.time.Clock()
        self.refresh(screen)

        MOVEEVENT, t, trail = pygame.USEREVENT+1, 250, []
        pygame.time.set_timer(MOVEEVENT, t, 0)
        running = True
        while running:
            self.draw_city(screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == MOVEEVENT:
                    self.refresh(screen)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                    elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.traffic_simulation.move_car(self.car_index, Location(2))
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.traffic_simulation.move_car(self.car_index, Location(3))
                    elif event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.traffic_simulation.move_car(self.car_index, Location(0))
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.traffic_simulation.move_car(self.car_index, Location(1))
                    elif event.key == pygame.K_h:
                        self.car_index = (self.car_index + 1) % len(self.traffic_simulation.cars) 

            
            self.traffic_simulation.car_at_destination(self.car_index)
            self.refresh(screen)
            pygame.display.flip()
            clock.tick(fps)
        print(f"{self.traffic_simulation.result()}: average time to destination")
        pygame.quit()



if __name__ == "__main__":
    gl = GameLoop()
    gl.start()
    