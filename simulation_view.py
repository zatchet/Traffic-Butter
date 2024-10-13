import pygame

from traffic_simulation import TrafficSimulation

#CONSTANTS
cellSize = 50 # pixels
black = (0, 0, 0)
white = (255, 255, 255)

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
        running = True
        while running:
            pygame.display.flip()
            clock.tick()



if __name__ == "__main__":
    gl = GameLoop()
    gl.start()
    