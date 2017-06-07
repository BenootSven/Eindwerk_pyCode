import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)


class Servo:
    def __init__(self, nServoPin, nHz):
        self.__ServoPin = nServoPin
        self.__Hz = nHz
        GPIO.setup(self.__ServoPin, GPIO.OUT)
        self.__servo = GPIO.PWM(self.__ServoPin, self.__Hz)

    def __str__(self):
        return "De ingegeven servo pin is: %s, de ingegeven frequentie is: %s (Range Servo van 0-13)" % (self.__ServoPin, self.__Hz)

    def init(self):
        self.__servo.start(12)

    def servoDakToe(self, delay=0.005, van=6.9, tot=12.0):
        teller1 = van
        while teller1 <= tot:
            self.__servo.ChangeDutyCycle(teller1)
            teller1 += 0.05
            time.sleep(delay)

    def servoDakOpen(self, delay=0.005, van=12.0, tot=6.9):
        teller2 = van
        while teller2 >= tot:
            self.__servo.ChangeDutyCycle(teller2)
            teller2 -= 0.05
            time.sleep(delay)

    def stopServo(self):
        self.__servo.ChangeDutyCycle(0)
        time.sleep(0.5)
        self.__servo.stop(0)
