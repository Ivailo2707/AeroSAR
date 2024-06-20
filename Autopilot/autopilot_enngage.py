from machine import Pin, PWM, UART
import time

input_pin = Pin(5, Pin.IN)
led = machine.Pin("LED", machine.Pin.OUT)
uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))

while True:
    while input_pin.value() == 0:
        pass
    start = time.ticks_us()
    while input_pin.value() == 1:
        pass
    end = time.ticks_us()
    duty = end - start
    print(str(duty))
    if duty >= 2000:
        led.on()
        uart.write('Duty above 2000\n')
    else:
        led.off()
