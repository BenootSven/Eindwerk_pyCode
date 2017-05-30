from Klassen.MCPklasse import SPI
from Klassen.I2CLCDklasse import i2cLCD
from Klassen.OneWireSensorKlasse import OneWireSensor
from Klassen.ServoEindwerkKlasse import Servo
import RPi.GPIO as GPIO
import time as delay

try:
    # toekenen van pinnen aan variabelen
    Rled = 16  # Pin toekenen voor Rood van ledstrip
    Gled = 12  # Pin toekenen voor Groen van ledstrip
    Bled = 25  # Pin toekenen voor Blauw van ledstrip
    Ventilator = 24  # Pin toekenen voor het besturen van de Ventilator
    IrigatiePomp = 23  # Pin toekenen voor het besturen van de Pomp
    servoPin = 18  # Pin toekenen voor Servo
    ListPinnen = [Rled, Gled, Bled, Ventilator, IrigatiePomp]
    # toekenen van input/output
    for pin in ListPinnen:
        GPIO.setup(pin, GPIO.OUT)
        print(pin)

    # initialiseren van klassen
    MCP = SPI()
    LCD = i2cLCD(0x27, 16)
    LCD.lcd_init()
    Onewire1 = OneWireSensor("/sys/bus/w1/devices/28-000008c5ac92/w1_slave")
    Onewire2 = OneWireSensor("/sys/bus/w1/devices/28-000008e097d8/w1_slave")
    servo = Servo(servoPin, 50)
    servo.init()


    # Klassen
    def ReadMoisture(channel):
        value = MCP.readChannel(channel)
        moisture = (value / 1023) * 100
        moisture = 100 - moisture
        return moisture


    # hoofdprogramma
    LCD.lcd_string("Proggramma gestart!", 0)
    while True:
        pass

except KeyboardInterrupt:
    print("\nProgramma manueel gestopt!")
    GPIO.cleanup()

except IOError:
    print("\nProgramma gestopt wegens I/O fout!")
    GPIO.cleanup()
