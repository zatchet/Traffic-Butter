import pygame
from intersection import StopLight, FourWayStopSign, TwoWayStopSign
from traffic_simulation import TrafficSimulation
from constants import *
       
# Represents all information to rendering the game
class GameLoop:
    def __init__(self):
        self.traffic_simulation = TrafficSimulation(num_of_cars=100)
        self.cell_size = min(MAX_SCREEN_SIZE // self.traffic_simulation.height, MAX_SCREEN_SIZE // self.traffic_simulation.width)
        self.screen_height = int(self.cell_size * self.traffic_simulation.height)
        self.screen_width = int(self.cell_size * self.traffic_simulation.width)
        self.CAR_SIZE = self.cell_size / 4

    def drawGrid(self, screen):
        for y in range(0, self.screen_height, self.cell_size):
            for x in range(0, self.screen_width, self.cell_size):
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, BLACK, rect, 1)   

    def drawCars(self, screen):
        for car in self.traffic_simulation.cars:
            x = car.curr_pos.x
            y = car.curr_pos.y
            location = car.on_side
            dir_val_x = location.math_dirs()[0]
            dir_val_y = location.math_dirs()[1]
            rect = pygame.Rect((x*self.cell_size) + (0 if (dir_val_x >= 0) else -self.CAR_SIZE), 
                               (y*self.cell_size) + (0 if (dir_val_y >= 0) else -self.CAR_SIZE), 
                               self.CAR_SIZE + (-abs(dir_val_y)*(self.CAR_SIZE/2)), 
                               self.CAR_SIZE + (-abs(dir_val_x)*(self.CAR_SIZE/2)))
            pygame.draw.rect(screen, car.color, rect, 0)
            pygame.draw.circle(screen, car.color,(((x*self.cell_size) + (dir_val_x*(self.CAR_SIZE*1.25))+ ((self.CAR_SIZE/4) if dir_val_x == 0 else 0)), 
                                                  ((y*self.cell_size) + (dir_val_y*(self.CAR_SIZE*1.25))+ ((self.CAR_SIZE/4) if dir_val_y == 0 else 0))), 
                                                  (self.CAR_SIZE/4))

    def draw_intersection_elements(self, screen):
        for y in range(1, self.traffic_simulation.height):
            for x in range(1, self.traffic_simulation.width):
                intersection = self.traffic_simulation.matrix[y][x]
                if type(intersection) == StopLight:
                    pygame.draw.circle(screen, GREEN if not intersection.y_axis_green else RED, ((x*self.cell_size) - (.1 * self.cell_size),(y * self.cell_size)), max(4, (self.cell_size / 20)))
                    pygame.draw.circle(screen, GREEN if not intersection.y_axis_green else RED, ((x*self.cell_size) + (.1 * self.cell_size),(y * self.cell_size)), max(4, (self.cell_size / 20)))
                    pygame.draw.circle(screen, GREEN if intersection.y_axis_green else RED, ((x*self.cell_size),(y * self.cell_size) - (.1 * self.cell_size)), max(4, (self.cell_size / 20)))
                    pygame.draw.circle(screen, GREEN if intersection.y_axis_green else RED, ((x*self.cell_size),(y * self.cell_size) + (.1 * self.cell_size)), max(4, (self.cell_size / 20)))
                if type(intersection) == FourWayStopSign:
                    rect = pygame.Rect((x*self.cell_size)-(.05 * self.cell_size),
                                       (y*self.cell_size)-(.05 * self.cell_size),
                                       max(8, (self.cell_size / 10)),
                                       max(8, (self.cell_size / 10)))
                    pygame.draw.rect(screen, RED, rect)
                if type(intersection) == TwoWayStopSign:
                    if intersection.y_axis_free:
                        pygame.draw.circle(screen, RED, ((x*self.cell_size) - (.1 * self.cell_size),(y * self.cell_size)), max(4, (self.cell_size / 20)))
                        pygame.draw.circle(screen, RED, ((x*self.cell_size) + (.1 * self.cell_size),(y * self.cell_size)), max(4, (self.cell_size / 20)))
                    else:
                        pygame.draw.circle(screen, RED, ((x*self.cell_size),(y * self.cell_size) - (.1 * self.cell_size)), max(4, (self.cell_size / 20)))
                        pygame.draw.circle(screen, RED, ((x*self.cell_size),(y * self.cell_size) + (.1 * self.cell_size)), max(4, (self.cell_size / 20)))

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
        screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Traffic Simulation")
        self.refresh(screen)

        while True:
            pygame.display.flip()
            self.refresh(screen)
            
            self.traffic_simulation.update_car_positions()
            
            if self.traffic_simulation.done():
                self.refresh(screen)
                result = self.traffic_simulation.result()
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
        
        print(f"average time to destination: {result} seconds")
        pygame.quit()

if __name__ == "__main__":
    gl = GameLoop()
    gl.start()
    