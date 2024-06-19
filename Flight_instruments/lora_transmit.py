import time
import board
import busio
from digitalio import DigitalInOut
import adafruit_rfm9x
import struct

from artificial_horizon import get_pitch_roll
from accelerometer import get_acceleration, get_speed
from thermal_camera import map_temperature_to_color, sensor

CS = DigitalInOut(board.CE1) 
RESET = DigitalInOut(board.D25)

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

try:
    rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0) 
    rfm9x.tx_power = 23
    print("RFM9x: Detected")
except RuntimeError as error:
    print("RFM9x: ERROR -", error)

def read_and_transmit_sensor_data():
    tr_pitch, tr_roll = get_pitch_roll()
    tr_xac, tr_yac, tr_zac = get_acceleration();
    temp_acceleration = get_acceleration()
    tr_speed = get_speed(temp_acceleration) - 3.5

    # tr_pitch = float(tr_pitch)
    # tr_roll = float(tr_roll)
   
    # tr_speed = float(tr_speed)

    temperatures = sensor.pixels 
    flat_temperatures = [temp for row in temperatures for temp in row]
    
    packet1 = struct.pack('6f32f', tr_pitch, tr_roll, tr_xac, tr_yac, tr_zac, tr_speed, *flat_temperatures[:32])
    packet2 = struct.pack('32f', *flat_temperatures[32:])
    
    rfm9x.send(packet1)
    time.sleep(0.1) 
    rfm9x.send(packet2)
    
    print("Data sent")

while True:
    #try:
        read_and_transmit_sensor_data()
        time.sleep(2)  # Transmit every 2 seconds
    # except Exception as e:
    #     print(f"Error: {e}")
    #     break
