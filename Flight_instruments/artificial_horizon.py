import smbus
import math
import pygame
import sys

bus = smbus.SMBus(1)

MPU6050_ADDRESS = 0x68
MPU6050_ACCEL_XOUT_H = 0x3B
MPU6050_GYRO_XOUT_H = 0x43

ACCEL_SCALE = 16384.0
GYRO_SCALE = 131.0

pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Artificial Horizon")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SKY_BLUE = (135, 206, 250)
DIRT_BROWN = (139, 69, 19)

def get_pitch_roll():
    accel_x = read_word_2c(MPU6050_ACCEL_XOUT_H)
    accel_y = read_word_2c(MPU6050_ACCEL_XOUT_H + 2)
    accel_z = read_word_2c(MPU6050_ACCEL_XOUT_H + 4)

    gyro_x = read_word_2c(MPU6050_GYRO_XOUT_H)
    gyro_y = read_word_2c(MPU6050_GYRO_XOUT_H + 2)
    gyro_z = read_word_2c(MPU6050_GYRO_XOUT_H + 4)

    accel_x /= ACCEL_SCALE
    accel_y /= ACCEL_SCALE
    accel_z /= ACCEL_SCALE

    gyro_x /= GYRO_SCALE
    gyro_y /= GYRO_SCALE
    gyro_z /= GYRO_SCALE

    roll = -math.atan2(accel_y, accel_z) * (180 / math.pi)
    pitch = math.atan(-accel_x / math.sqrt(accel_y**2 + accel_z**2)) * (180 / math.pi)

    return roll, pitch

def read_word(reg):
    high = bus.read_byte_data(MPU6050_ADDRESS, reg)
    low = bus.read_byte_data(MPU6050_ADDRESS, reg + 1)
    value = (high << 8) + low
    return value

def read_word_2c(reg):
    val = read_word(reg)
    if val >= 0x8000:
        return -((65535 - val) + 1)
    else:
        return val

# def draw_artificial_horizon(roll, pitch):
#     horizon_line_length = 50
#     horizon_line_thickness = 5

#     screen.fill(DIRT_BROWN)

#     sky_height = int(HEIGHT // 2 - pitch)
#     ground_height = int(HEIGHT // 2 + pitch)

#     pygame.draw.rect(screen, SKY_BLUE, (0, 0, WIDTH, sky_height))
#     pygame.draw.rect(screen, DIRT_BROWN, (0, HEIGHT - ground_height, WIDTH, ground_height))

#     airplane_icon = pygame.image.load("airplane.bmp")
#     airplane_icon = pygame.transform.scale(airplane_icon, (150, 150))
#     rotated_airplane = pygame.transform.rotate(airplane_icon, roll)
#     airplane_rect = rotated_airplane.get_rect(center=(WIDTH // 2, HEIGHT // 2))
#     screen.blit(rotated_airplane, airplane_rect.topleft)

#     font = pygame.font.Font(None, 36)
#     text_pitch = font.render(f"Pitch: {pitch:.2f} degrees", True, WHITE)
#     text_roll = font.render(f"Roll: {roll:.2f} degrees", True, WHITE)

#     screen.blit(text_pitch, (10, 10))
#     screen.blit(text_roll, (10, 50))

#     pygame.display.flip()

# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()

#     roll_angle, pitch_angle = get_pitch_roll()

#     draw_artificial_horizon(roll_angle, pitch_angle)
