import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
fan = 16
pump = 12
Gled = 25
Bled = 24
Rled = 23
GPIO.setup(fan, GPIO.OUT)
GPIO.setup(pump, GPIO.OUT)
GPIO.setup(Rled, GPIO.OUT)
GPIO.setup(Gled, GPIO.OUT)
GPIO.setup(Bled, GPIO.OUT)
GPIO.output(Rled, GPIO.LOW)
GPIO.output(Gled, GPIO.LOW)
GPIO.output(Bled, GPIO.LOW)
GPIO.output(pump, GPIO.LOW)
GPIO.output(fan, GPIO.LOW)
GPIO.cleanup()