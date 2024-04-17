import RPi.GPIO as GPIO
from time import sleep
from communication import is_autopilot_engaged

GPIO.setmode(GPIO.BOARD)

SERVO_PINS = [17, 22, 27]

for pin in SERVO_PINS:
    GPIO.setup(pin, GPIO.OUT)


pwms = [GPIO.PWM(pin, 50) for pin in SERVO_PINS]
for pwm in pwms:
    pwm.start(0)

def setAngle(pin, angle):
    duty = angle / 18 + 2
    GPIO.output(pin, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(pin, False)
    pwm.ChangeDutyCycle(duty)

def autopilot_circle_mode(pitch, roll):
    if is_autopilot_engaged():
        setAngle(22, 45)

        if pitch < 0:
            while pitch != 0:
                setAngle(27, 45)
                if pitch == 0:
                    setAngle(27, 90)
                    break
        
        elif pitch > 0:
            while pitch != 0:
                setAngle(27, 135)
                if pitch == 0:
                    setAngle(27, 90)
                    break
        
        if roll < 0:
            while roll != 0:
                setAngle(17, 45)
                if roll == 0:
                    setAngle(17, 90)
                    break
        
        elif roll > 0:
            while roll != 0:
                setAngle(27, 135)
                if roll == 0:
                    setAngle(27, 90)
                    break
    else:
        return
                

        

    