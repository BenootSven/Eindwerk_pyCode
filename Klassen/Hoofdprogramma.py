from Klassen.I2CLCDklasse import i2cLCD
from Klassen.MCPklasse import SPI
from Klassen.ServoEindwerkKlasse import Servo
from Klassen.OneWireSensorKlasse import OneWireSensor
import time
from Klassen.class_db import DbClass
import RPi.GPIO as GPIO

db = DbClass()

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

LCD = i2cLCD(0x27, 16)
LCD.lcd_init()

MCP = SPI()

onewire1 = OneWireSensor('/sys/bus/w1/devices/28-000008c5ac92/w1_slave')
onewire2 = OneWireSensor('/sys/bus/w1/devices/28-000008e097d8/w1_slave')

servo = Servo(18, 50)
servo.init()


class Main():
    def __init__(self):
        self.TempVorige = 0
        self.HumVorige = 0

    def MainProgram(self):
        try:

            vochtZone1 = round((100 - (MCP.readChannel(0) / 1023) * 100), 2)
            vochtZone2 = round((100 - (MCP.readChannel(1) / 1023) * 100), 2)
            tempBinnen = round(onewire1.read_temp(), 2)

            settings = db.getOneSingleRowData("Settings")
            for setting in settings:
                Temp = int(setting[1])
                Hum = int(setting[2])

            if tempBinnen >= Temp:
                LCD.lcd_clear()
                GPIO.output(fan, GPIO.HIGH)
                servo.servoDakOpen(0.03)
                LCD.lcd_string("Last update:", 0)
                LCD.lcd_string("Temp te hoog", 1)
            else:
                LCD.lcd_clear()
                GPIO.output(fan, GPIO.LOW)
                servo.servoDakToe(0.03)
                LCD.lcd_string("Last update:", 0)
                LCD.lcd_string("Temp normaal", 1)

            if vochtZone1 < Hum or vochtZone2 < Hum:
                LCD.lcd_clear()
                GPIO.output(pump, GPIO.HIGH)
                LCD.lcd_string("Last update:", 0)
                LCD.lcd_string("Hum te laag", 1)
            else:
                LCD.lcd_clear()
                GPIO.output(pump, GPIO.LOW)
                LCD.lcd_string("Last update:", 0)
                LCD.lcd_string("Hum normaal", 1)

        except:
            print("Main program error")
