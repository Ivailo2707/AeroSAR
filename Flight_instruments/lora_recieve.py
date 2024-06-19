import time
import board
import busio
from digitalio import DigitalInOut
import adafruit_rfm9x
import struct
import pygame
import sys

import random

CS = DigitalInOut(board.CE1)  
RESET = DigitalInOut(board.D25) 
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

try:
    rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
    print("RFM9x: Detected and initialized")
except RuntimeError as error:
    print("RFM9x: ERROR -", error)
    sys.exit(1)

def receive_and_process_data():
    packet1 = rfm9x.receive(timeout=5.0)
    if packet1 is None:
        print("No data received")
        return None
    
    packet2 = rfm9x.receive(timeout=5.0)
    if packet2 is None:
        print("Incomplete data received")
        return None
    
    try:
        unpacked_data1 = struct.unpack('6f32f', packet1)
        tr_pitch, tr_roll, x_accel, y_accel, z_accel, tr_speed = unpacked_data1[:6]
        temperatures1 = unpacked_data1[6:]
        
        temperatures2 = struct.unpack('32f', packet2)
        
        temperatures = temperatures1 + temperatures2 
        temp_matrix = [temperatures[i:i + 8] for i in range(0, 64, 8)]
        
        return (tr_pitch, tr_roll, x_accel, y_accel, z_accel, tr_speed), temp_matrix
    except struct.error as e:
        print(f"Error unpacking data: {e}")
        return None

WINDOW_WIDTH = 1000  
WINDOW_HEIGHT = 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 250)
DIRT_BROWN = (139, 69, 19)
ARTIFICIAL_HORIZON_WIDTH = 400
ARTIFICIAL_HORIZON_HEIGHT = 400
SENSOR_COLS = 8
SENSOR_ROWS = 8
CELL_SIZE = 40
THERMAL_CAMERA_WIDTH = SENSOR_COLS * CELL_SIZE
THERMAL_CAMERA_HEIGHT = SENSOR_ROWS * CELL_SIZE

pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Flight Instruments")

artificial_horizon_area = pygame.Rect(50, 50, ARTIFICIAL_HORIZON_WIDTH, ARTIFICIAL_HORIZON_HEIGHT)
thermal_camera_area = pygame.Rect(500, 50, THERMAL_CAMERA_WIDTH, THERMAL_CAMERA_HEIGHT)

# def generate_test_data():
#     tr_pitch = random.uniform(-10, 10)  
#     tr_roll = random.uniform(-30, 30)  
#     x_accel = random.uniform(-5, 5)     
#     y_accel = random.uniform(-5, 5)
#     z_accel = random.uniform(-5, 5)
#     tr_speed = random.uniform(0, 200)  
    
#     # Generate a simulated 8x8 temperature matrix
#     temp_matrix = [[random.uniform(20, 40) for _ in range(SENSOR_COLS)] for _ in range(SENSOR_ROWS)]
    
#     return (tr_pitch, tr_roll, x_accel, y_accel, z_accel, tr_speed), temp_matrix

def map_temperature_to_color(temp):
    blue = 255 - int((temp - 20) * (255 / 20))
    red = int((temp - 20) * (255 / 20))
    return red, 0, blue

def draw_artificial_horizon(screen, roll, pitch, speed):
    screen.fill(DIRT_BROWN, artificial_horizon_area)
    
    horizon_center_x = artificial_horizon_area.centerx
    horizon_center_y = artificial_horizon_area.centery
    
    sky_height = int(artificial_horizon_area.height // 2 - pitch)
    ground_height = int(artificial_horizon_area.height // 2 + pitch)
    
    pygame.draw.rect(screen, SKY_BLUE, (artificial_horizon_area.x, artificial_horizon_area.y,
                                         artificial_horizon_area.width, sky_height))
    pygame.draw.rect(screen, DIRT_BROWN, (artificial_horizon_area.x,
                                          artificial_horizon_area.y + artificial_horizon_area.height - ground_height,
                                          artificial_horizon_area.width, ground_height))
    
    airplane_icon = pygame.image.load("airplane.bmp")
    airplane_icon = pygame.transform.scale(airplane_icon, (150, 150))
    rotated_airplane = pygame.transform.rotate(airplane_icon, roll)
    airplane_rect = rotated_airplane.get_rect(center=(horizon_center_x, horizon_center_y))
    screen.blit(rotated_airplane, airplane_rect)
    
    font = pygame.font.Font(None, 24)
    text_pitch = font.render(f"Pitch: {pitch:.2f} degrees", True, WHITE)
    text_roll = font.render(f"Roll: {roll:.2f} degrees", True, WHITE)
    text_speed = font.render(f"Speed: {speed:.2f} km/h", True, WHITE)
    
    screen.blit(text_pitch, (artificial_horizon_area.x + 10, artificial_horizon_area.y + 10))
    screen.blit(text_roll, (artificial_horizon_area.x + 10, artificial_horizon_area.y + 40))
    screen.blit(text_speed, (artificial_horizon_area.x + 10, artificial_horizon_area.y + 70))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #sensor_data = generate_test_data()
    sensor_data = receive_and_process_data()
    if sensor_data is not None:
        (tr_pitch, tr_roll, x_accel, y_accel, z_accel, tr_speed), temp_matrix = sensor_data

        draw_artificial_horizon(window, tr_roll, tr_pitch, tr_speed)  

        window.fill(WHITE, thermal_camera_area)
        for x in range(SENSOR_COLS):
            for y in range(SENSOR_ROWS):
                temp = temp_matrix[y][x]
                color = map_temperature_to_color(temp)
                pygame.draw.rect(window, color, (thermal_camera_area.x + x * CELL_SIZE, thermal_camera_area.y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        pygame.display.update()
    time.sleep(2)

pygame.quit()
