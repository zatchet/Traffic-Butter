import pygame
from intersection import StopLight, FourWayStopSign, TwoWayStopSign
from traffic_simulation import TrafficSimulation
from constants import *
from direction import Direction
# Represents all information to rendering the game

class SimulationView:
    def __init__(self, traffic_simulation: TrafficSimulation, draw_cars: bool = True):
        self.draw_cars = draw_cars
        self.traffic_simulation = traffic_simulation
        self.cell_size = min(MAX_SCREEN_SIZE // (self.traffic_simulation.height + 1), MAX_SCREEN_SIZE // (self.traffic_simulation.width + 1))
        self.screen_height = int(self.cell_size * (self.traffic_simulation.height + 1))
        self.screen_width = int(self.cell_size * (self.traffic_simulation.width + 1))
        self.car_length = self.cell_size / 4
        self.car_width = self.car_length / 2

    def drawGrid(self, screen):
        for y in range(0, self.screen_height, self.cell_size):
            for x in range(0, self.screen_width, self.cell_size):
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, BLACK, rect, 1)   

    def drawCars(self, screen):
        for car in self.traffic_simulation.cars:
            x, y = car.curr_pos.x + 1, car.curr_pos.y + 1
            direction = car.on_side
            triangle_length = self.car_width

            if direction == Direction.up:
                rect = pygame.Rect((x*self.cell_size), (y*self.cell_size) + 2*triangle_length, self.car_width, self.car_length)
                triangle_points = [(x*self.cell_size, y*self.cell_size + 2*triangle_length),
                      (x*self.cell_size + triangle_length, y*self.cell_size + 2*triangle_length),
                      (x*self.cell_size + triangle_length/2, y*self.cell_size + triangle_length)]
            if direction == Direction.down:
                rect = pygame.Rect((x*self.cell_size) - self.car_width, (y*self.cell_size) - self.car_length - 2*triangle_length, self.car_width, self.car_length)
                triangle_points = [(x*self.cell_size - triangle_length, y*self.cell_size - 2*triangle_length),
                      (x*self.cell_size, y*self.cell_size - 2*triangle_length),
                      (x*self.cell_size - triangle_length/2, y*self.cell_size - triangle_length)]
            if direction == Direction.left:
                rect = pygame.Rect((x*self.cell_size) + 2*triangle_length, (y*self.cell_size) - self.car_width, self.car_length, self.car_width)
                triangle_points = [(x*self.cell_size + 2*triangle_length, y*self.cell_size),
                      (x*self.cell_size + 2*triangle_length, y*self.cell_size - triangle_length),
                      (x*self.cell_size + triangle_length, y*self.cell_size - triangle_length/2)]
            if direction == Direction.right:
                rect = pygame.Rect((x*self.cell_size) - self.car_length - 2*triangle_length, (y*self.cell_size), self.car_length, self.car_width)
                triangle_points = [(x*self.cell_size - 2*triangle_length, y*self.cell_size),
                      (x*self.cell_size - 2*triangle_length, y*self.cell_size + triangle_length),
                      (x*self.cell_size - triangle_length, y*self.cell_size + triangle_length/2)]
            
            pygame.draw.rect(screen, car.color, rect, 5)
            pygame.draw.polygon(screen, car.color, triangle_points, 5)

    def draw_intersection_elements(self, screen):
        for y_matrix in range(0, self.traffic_simulation.height):
            for x_matrix in range(0, self.traffic_simulation.width):
                intersection = self.traffic_simulation.matrix[y_matrix][x_matrix]
                x, y = x_matrix + 1, y_matrix + 1
                if type(intersection) == StopLight:
                    pygame.draw.circle(screen, GREEN if not intersection.y_axis_green else RED, ((x*self.cell_size) - (.1 * self.cell_size),(y * self.cell_size)), max(4, (self.cell_size / 20)))
                    pygame.draw.circle(screen, GREEN if not intersection.y_axis_green else RED, ((x*self.cell_size) + (.1 * self.cell_size),(y * self.cell_size)), max(4, (self.cell_size / 20)))
                    pygame.draw.circle(screen, GREEN if intersection.y_axis_green else RED, ((x*self.cell_size),(y * self.cell_size) - (.1 * self.cell_size)), max(4, (self.cell_size / 20)))
                    pygame.draw.circle(screen, GREEN if intersection.y_axis_green else RED, ((x*self.cell_size),(y * self.cell_size) + (.1 * self.cell_size)), max(4, (self.cell_size / 20)))
                if type(intersection) == FourWayStopSign:
                    width = max(8, (self.cell_size / 10))
                    rect = pygame.Rect((x*self.cell_size)-(.05 * self.cell_size), (y*self.cell_size)-(.05 * self.cell_size), width, width)
                    pygame.draw.rect(screen, RED, rect)
                if type(intersection) == TwoWayStopSign:
                    width = max(8, (self.cell_size / 12))
                    if intersection.y_axis_free:
                        rect1 = pygame.Rect(x*self.cell_size - .09 * self.cell_size - width/2, y * self.cell_size - width/2, width, width)
                        rect2 = pygame.Rect(x*self.cell_size + .09 * self.cell_size - width/2, y * self.cell_size - width/2, width, width)
                    else:
                        rect1 = pygame.Rect(x*self.cell_size - width/2, y * self.cell_size - .09 * self.cell_size - width/2, width, width)
                        rect2 = pygame.Rect(x*self.cell_size - width/2, y * self.cell_size + .09 * self.cell_size - width/2, width, width)
                    pygame.draw.rect(screen, RED, rect1)
                    pygame.draw.rect(screen, RED, rect2)

    # begins the simuation
    def start(self):
        return self.loop_gui()

    def refresh(self, screen):
        screen.fill(WHITE)
        self.draw_city(screen)

    def draw_city(self, screen):
        self.drawGrid(screen)
        if self.draw_cars:
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
                self.drawCars(screen)
                result = self.traffic_simulation.result()
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

        pygame.quit()
        return result
    
if __name__ == "__main__":
    view = SimulationView(TrafficSimulation(num_of_cars=5), draw_cars=True)
    view.start()
    