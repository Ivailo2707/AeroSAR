import smbus
import math
import time

MPU6050_ADDRESS = 0x68

MPU6050_ACCEL_XOUT_H = 0x3B
MPU6050_ACCEL_YOUT_H = 0x3D
MPU6050_ACCEL_ZOUT_H = 0x3F

bus = smbus.SMBus(1)

def read_word_2c(address):
    high = bus.read_byte_data(MPU6050_ADDRESS, address)
    low = bus.read_byte_data(MPU6050_ADDRESS, address+1)
    val = (high << 8) + low
    if val >= 0x8000:
        return -((65535 - val) + 1)
    else:
        return val

def get_acceleration():
    x_accel = read_word_2c(MPU6050_ACCEL_XOUT_H) / 16384.0
    y_accel = read_word_2c(MPU6050_ACCEL_YOUT_H) / 16384.0
    z_accel = read_word_2c(MPU6050_ACCEL_ZOUT_H) / 16384.0
    return x_accel, y_accel, z_accel

def get_speed(acceleration):
    speed_mps = math.sqrt(acceleration[0]**2 + acceleration[1]**2 + acceleration[2]**2)
    speed_kph = speed_mps * 3.6
    return speed_kph

if __name__ == "__main__":
    while True:
        acceleration = get_acceleration()
        speed = get_speed(acceleration)-(3.5)
        if(speed < 0):
            speed = 0

        print("Speed: %.2f km/h" % speed)

        time.sleep(1)
