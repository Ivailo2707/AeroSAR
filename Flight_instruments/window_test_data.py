import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the window
WINDOW_WIDTH = 1000  # Increased width to accommodate the new section
WINDOW_HEIGHT = 400
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Combined Pygame Windows")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 250)
DIRT_BROWN = (139, 69, 19)

# Artificial Horizon parameters
ARTIFICIAL_HORIZON_WIDTH = 400
ARTIFICIAL_HORIZON_HEIGHT = 400
artificial_horizon_area = pygame.Rect(50, 50, ARTIFICIAL_HORIZON_WIDTH, ARTIFICIAL_HORIZON_HEIGHT)

# Thermal Camera parameters
SENSOR_COLS = 8
SENSOR_ROWS = 8
cell_size = 40
THERMAL_CAMERA_WIDTH = SENSOR_COLS * cell_size
THERMAL_CAMERA_HEIGHT = SENSOR_ROWS * cell_size
thermal_camera_area = pygame.Rect(500, 50, THERMAL_CAMERA_WIDTH, THERMAL_CAMERA_HEIGHT)

# Functions for the Thermal Camera visualization
def map_temperature_to_color(temp):
    blue = 255 - int((temp - 20) * (255 / 20))
    red = int((temp - 20) * (255 / 20))
    return red, 0, blue

# Simulate thermal camera data
def simulate_thermal_data():
    return [[random.uniform(20, 40) for _ in range(SENSOR_COLS)] for _ in range(SENSOR_ROWS)]

# Function to draw artificial horizon
def draw_artificial_horizon(screen, roll, pitch, speed, altitude):
    horizon_line_length = 50
    horizon_line_thickness = 5

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

    # Load airplane image
    airplane_icon = pygame.image.load("airplane.bmp")
    airplane_icon = pygame.transform.scale(airplane_icon, (150, 150))
    rotated_airplane = pygame.transform.rotate(airplane_icon, roll)
    airplane_rect = rotated_airplane.get_rect(center=(horizon_center_x, horizon_center_y))
    screen.blit(rotated_airplane, airplane_rect)

    # Draw pitch and roll text
    font = pygame.font.Font(None, 24)
    text_pitch = font.render(f"Pitch: {pitch:.2f} degrees", True, WHITE)
    text_roll = font.render(f"Roll: {roll:.2f} degrees", True, WHITE)
    text_speed = font.render(f"Speed: {speed} mph", True, WHITE)
    text_altitude = font.render(f"Altitude: {altitude} ft", True, WHITE)

    screen.blit(text_pitch, (artificial_horizon_area.x + 10, artificial_horizon_area.y + 10))
    screen.blit(text_roll, (artificial_horizon_area.x + 10, artificial_horizon_area.y + 40))
    screen.blit(text_speed, (artificial_horizon_area.x + 10, artificial_horizon_area.y + 70))
    screen.blit(text_altitude, (artificial_horizon_area.x + 10, artificial_horizon_area.y + 100))

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Artificial Horizon visualization
    # Simulated pitch, roll, speed, and altitude values
    draw_artificial_horizon(window, 0, 0, 150, 10000)  

    # Thermal Camera visualization
    window.fill(WHITE, thermal_camera_area)
    temperatures = simulate_thermal_data()
    for x in range(SENSOR_COLS):
        for y in range(SENSOR_ROWS):
            temp = temperatures[y][x]
            color = map_temperature_to_color(temp)
            pygame.draw.rect(window, color, (thermal_camera_area.x + x * cell_size, thermal_camera_area.y + y * cell_size, cell_size, cell_size))

    # Update the display
    pygame.display.update()

pygame.quit()
