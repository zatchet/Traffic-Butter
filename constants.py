LIGHT_RELEASE_RATE = 1 # when the light turns green, cars that were in queue go through it every LIGHT_RELEASE_RATE seconds
STOP_SIGN_RELEASE_RATE = 2 # every STOP_SIGN_RELEASE_RATE seconds, a car is released from the stop sign
LEFT_TURN_PENALTY = 0.5 # when a car turns left, it has to wait an additional LEFT_TURN_PENALTY seconds
MOVEMENT_DELAY = 0.5 # time it takes a car to move one cell (e.g. through a green light)

GRID_SIZE_Y = 10
GRID_SIZE_X = 10
MAX_SCREEN_SIZE = 800 # Max size the grid can be (axis agnostic)
BLACK = (0, 0, 0)

WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
RED = (255, 0, 0)

CAR_COLORS = ['blue4', 'blueviolet', 'chocolate', 'deeppink4', 'coral2', 'darkturquoise', 'goldenrod4', 'gray46', 'lightseagreen', 'violetred4', 'yellow3', 'slateblue3']

# A* route-finding constants
STOP_LIGHT_COST = 2.0
FOUR_WAY_STOP_SIGN_COST = 1.5
TWO_WAY_STOP_SIGN_COST = 1.5