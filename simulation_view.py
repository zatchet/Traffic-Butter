import pygame
import time
from Location import Location
from traffic_simulation import TrafficSimulation

#CONSTANTS
cellSize = 50 # pixels
black = (0, 0, 0)
a_color = (53, 63, 231)
white = (255, 255, 255)
fps = 60

# Represents all information to rendering the game
class GameLoop:
    def __init__(self):
        self.traffic_simulation = TrafficSimulation()
        self.screen_height = cellSize * self.traffic_simulation.height
        self.screen_width = cellSize * self.traffic_simulation.width

    def drawGrid(self, screen):
        for y in range(0, self.screen_height, cellSize):
            for x in range(0, self.screen_width, cellSize):
                rect = pygame.Rect(x, y, cellSize, cellSize)
                pygame.draw.rect(screen, black, rect, 1)   

    def drawCars(self, screen):
        for car in self.traffic_simulation.cars:
            x = car.curr_pos.x
            y = car.curr_pos.y
            location = car.on_side
            dir_val_x = location.math_dirs()[0]
            dir_val_y = location.math_dirs()[1]
            print(location)
            print(car)
            #if location == Location.left or location == Location.right:
            rect = pygame.Rect((x*cellSize) + (0 if (dir_val_x >= 0) else -20), (y*cellSize) + (0 if (dir_val_y >= 0) else -20), 20 + (-abs(dir_val_y)*10) , 20 + (-abs(dir_val_x)*10))
            #rect = pygame.Rect((x*cellSize) + (dir_val_x * 20), (y*cellSize) + (dir_val_y * 20), 20 + (-abs(dir_val_y)*10), )
            pygame.draw.rect(screen, a_color, rect, 5)

    # begins the simuation
    def start(self):
        self.loop_gui()
        
    def loop_gui(self):
        pygame.init()
        screen = pygame.display.set_mode((self.screen_height, self.screen_width))
        pygame.display.set_caption("Traffic Simulation")
        clock = pygame.time.Clock()
        screen.fill(white)

        self.drawGrid(screen)
        self.drawCars(screen)
        running = True
        while running:
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
            pygame.display.flip()
            clock.tick(fps)
        pygame.quit()



if __name__ == "__main__":
    gl = GameLoop()
    gl.start()
    