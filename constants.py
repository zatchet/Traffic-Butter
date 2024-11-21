LIGHT_RELEASE_RATE = 1 # when the light is green, cars go through it every LIGHT_RELEASE_RATE seconds
STOP_SIGN_RELEASE_RATE = 2 # every STOP_SIGN_RELEASE_RATE seconds, a car is released from the stop sign
MINIMUM_STOP_SIGN_WAIT_TIME = 1 # if a car arrives at an empty stop sign, it must wait at least MINIMUM_STOP_SIGN_WAIT_TIME seconds before it can be released

CELL_SIZE = 75 # pixels
CAR_SIZE = 20
BLACK = (0, 0, 0)

WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
RED = (255, 0, 0)

CAR_COLORS = [(134, 56, 210), (29, 254, 155), (98, 92, 9), (20, 25, 253), (24, 121, 41), (123, 245, 86), (155, 194, 214), (46, 163, 45), (253, 221, 106), (37, 38, 175)]