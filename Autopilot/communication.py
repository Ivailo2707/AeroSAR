import RPi.GPIO as GPIO
import time

def is_autopilot_engaged():
    GPIO.setmode(GPIO.BCM)
    SWITCH_PIN = 13  
    GPIO.setup(SWITCH_PIN, GPIO.IN)

    last_time = time.time()
    last_state = GPIO.input(SWITCH_PIN)
    
    current_time = time.time()
    current_state = GPIO.input(SWITCH_PIN)
    
    if current_state != last_state and current_state == GPIO.HIGH:
        pulse_duration = current_time - last_time
        
        if pulse_duration >= 1 and pulse_duration <= 2:
            GPIO.cleanup()
            return True
    
    GPIO.cleanup()
    return False



        