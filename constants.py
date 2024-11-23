LIGHT_RELEASE_RATE = 1 # when the light is green, cars go through it every LIGHT_RELEASE_RATE seconds
STOP_SIGN_RELEASE_RATE = 2 # every STOP_SIGN_RELEASE_RATE seconds, a car is released from the stop sign
LEFT_TURN_PENALTY = 0.5 # when a car turns left, it has to wait an additional LEFT_TURN_PENALTY seconds
GRID_SIZE_Y = 10
GRID_SIZE_X = 10
MAX_SCREEN_SIZE = 1200 # Max size the grid can be (axis agnostic)
BLACK = (0, 0, 0)

WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
RED = (255, 0, 0)

CAR_COLORS = [(134, 56, 210), (29, 254, 155), (98, 92, 9), (20, 25, 253), (24, 121, 41), (123, 245, 86), (155, 194, 214), (46, 163, 45), (253, 221, 106), (37, 38, 175)]

# A* route-finding constants
STOP_LIGHT_COST = 2.0
FOUR_WAY_STOP_SIGN_COST = 1.5
TWO_WAY_STOP_SIGN_COST = 1.5