import pygame
import board
import busio
import adafruit_amg88xx
from colour import Color

i2c_bus = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_amg88xx.AMG88XX(i2c_bus)

SENSOR_COLS = 8
SENSOR_ROWS = 8

#pygame.init()

cell_size = 40
display_width = SENSOR_COLS * cell_size
display_height = SENSOR_ROWS * cell_size
#game_display = pygame.display.set_mode((display_width, display_height))
#pygame.display.set_caption('Thermal Camera')

blue = Color("blue")
red = Color("red")
gradient = list(blue.range_to(red, 50))

def map_temperature_to_color(temp):
    blue = Color("blue")
    red = Color("red")
    gradient = list(blue.range_to(red, 50))

    temp_min = 20.0 
    temp_max = 40.0
    index = int((temp - temp_min) / (temp_max - temp_min) * len(gradient))
    index = max(0, min(index, len(gradient) - 1))

    return tuple(int(c * 255) for c in gradient[index].rgb)


# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     temperatures = sensor.pixels

#     game_display.fill((0, 0, 0)) 

#     for x in range(SENSOR_COLS):
#         for y in range(SENSOR_ROWS):
#             temp = temperatures[y][x]
#             color = map_temperature_to_color(temp)
#             pygame.draw.rect(game_display, color, (x * cell_size, y * cell_size, cell_size, cell_size))

#     pygame.display.update()

# pygame.quit()
