import serial
import time

ser = serial.Serial('/dev/serial0', 115200, timeout=1)

while True:
    if ser.in_waiting > 0:
        try:
            line = ser.readline().decode('utf-8').strip()
            print(line)
            if line == 'Duty above 2000':
                print('Received message: Duty cycle is above 2000')
        except UnicodeDecodeError as e:
            print(f"Decoding error: {e}. Raw data: {ser.readline()}")
        time.sleep(0.1)
