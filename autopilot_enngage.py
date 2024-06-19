from machine import Pin, PWM
import time

input_pin  = Pin(5, Pin.IN)
led = machine.Pin("LED", machine.Pin.OUT)
while True:
    while input_pin.value() == 0:
        pass
    start = time.ticks_us()
    while input_pin.value() == 1:
        pass
    end = time.ticks_us()
    duty = end - start
    print (str(duty))
    if duty >= 2000:
        led.on()
    else:
        led.off()