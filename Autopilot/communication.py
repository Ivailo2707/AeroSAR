import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
SWITCH_PIN = 13  
GPIO.setup(SWITCH_PIN, GPIO.IN)


last_time = time.time()
last_state = GPIO.input(SWITCH_PIN)

try:
    while True:
        current_time = time.time()
        current_state = GPIO.input(SWITCH_PIN)
        
        if current_state != last_state and current_state == GPIO.HIGH:
            pulse_duration = current_time - last_time
            
            if pulse_duration >= 1 and pulse_duration <= 2:
                print("Switch flicked")
        
        last_state = current_state
        last_time = current_time
        
        time.sleep(0.01)  

except KeyboardInterrupt:
    GPIO.cleanup()  
        