from flask import Flask, render_template, request, redirect
from Klassen.I2CLCDklasse import i2cLCD
from Klassen.MCPklasse import SPI
from Klassen.ServoEindwerkKlasse import Servo
from Klassen.OneWireSensorKlasse import OneWireSensor
import threading
from Klassen.class_db import DbClass
import RPi.GPIO as GPIO
from Klassen.Hoofdprogramma import Main
import time

State = 0
StateWeergave = "Automatic"

db = DbClass()

Program = Main()

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

servo = Servo(18, 50)
servo.init()

onewire1 = OneWireSensor('/sys/bus/w1/devices/28-000008c5ac92/w1_slave')
onewire2 = OneWireSensor('/sys/bus/w1/devices/28-000008e097d8/w1_slave')

app = Flask(__name__)


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def MainProgram():
    t = threading.currentThread()
    print("###Hoofdprogramma gestart###")
    while getattr(t, "do_run", True):
        Program.MainProgram()
    GPIO.output(pump, GPIO.LOW)
    GPIO.output(fan, GPIO.LOW)
    servo.servoDakToe(0.03)
    print("###Hoofdprogramma gestopt###")


def DataLogging():
    t = threading.currentThread()
    print("###Datalogging Gestart###")
    while getattr(t, "do_run", True):
        vocht1 = round((100 - (MCP.readChannel(0) / 1023) * 100), 2)
        vocht2 = round((100 - (MCP.readChannel(1) / 1023) * 100), 2)
        temp1 = round(onewire1.read_temp(), 2)
        temp2 = round(onewire2.read_temp(), 2)
        db.TempToDatabase(temp1, temp2)
        db.HumidityToDatabase(vocht1, vocht2)
        time.sleep(4)
        print("Data Logged!")
    print("###Datalogging gestopt###")


t = threading.Thread(target=MainProgram)
t.start()

t2 = threading.Thread(target=DataLogging)
t2.start()


@app.route('/')
def Home():
    global StateWeergave
    temp = db.getDataFromDatabase("Temperature")
    humidity = db.getDataFromDatabase("Humidity")
    statetemp = db.getOneSingleRowData("Temperature")
    statehumidity = db.getOneSingleRowData("Humidity")
    return render_template("Home.html", Temp=temp, Humidity=humidity, StateTemp=statetemp, StateHumidity=statehumidity, state=StateWeergave)


@app.route('/setGPIO', methods=['POST'])
def handle_data():
    global State, StateWeergave, t
    tekst = request.form['value_set']
    if State != int(tekst) and tekst != " " and (tekst == "1" or tekst == "0"):
        State = int(tekst)
        if State == 0:
            StateWeergave = "Automatic"
            t = threading.Thread(target=MainProgram)
            t.start()

        if State == 1:
            StateWeergave = "Manual"
            t.do_run = False
            t.join()

    if State == 1:
        if tekst == "11":
            LCD.lcd_clear()
            LCD.lcd_string("Last update:", 0)
            LCD.lcd_string("pomp aan", 1)
            GPIO.output(pump, GPIO.HIGH)

        if tekst == "10":
            LCD.lcd_clear()
            LCD.lcd_string("Last update:", 0)
            LCD.lcd_string("pomp uit", 1)
            GPIO.output(pump, GPIO.LOW)

        if tekst == "21":
            LCD.lcd_clear()
            LCD.lcd_string("Last update:", 0)
            LCD.lcd_string("ventilator aan", 1)
            GPIO.output(fan, GPIO.HIGH)

        if tekst == "20":
            LCD.lcd_clear()
            LCD.lcd_string("Last update:", 0)
            LCD.lcd_string("ventilator uit", 1)
            GPIO.output(fan, GPIO.LOW)

        if tekst == "31":
            LCD.lcd_clear()
            LCD.lcd_string("Last update:", 0)
            LCD.lcd_string("LED aan", 1)
            GPIO.output(Rled, GPIO.HIGH)
            GPIO.output(Gled, GPIO.HIGH)
            GPIO.output(Bled, GPIO.HIGH)

        if tekst == "30":
            LCD.lcd_clear()
            LCD.lcd_string("Last update:", 0)
            LCD.lcd_string("LED uit", 1)
            GPIO.output(Rled, GPIO.LOW)
            GPIO.output(Gled, GPIO.LOW)
            GPIO.output(Bled, GPIO.LOW)

        if tekst == "41":
            LCD.lcd_clear()
            LCD.lcd_string("Last update:", 0)
            LCD.lcd_string("Dak open", 1)
            servo.servoDakOpen(0.03)

        if tekst == "40":
            LCD.lcd_clear()
            LCD.lcd_string("Last update:", 0)
            LCD.lcd_string("Dak toe", 1)
            servo.servoDakToe(0.03)

    return redirect("/")


@app.route('/details')
def Details():
    data = db.getDetailsFromDatabase("Temperature")
    lijst = []
    for Temp in data:
        lijst.append(Temp[1])
    return render_template("Details.html", Data=lijst)


@app.route('/details2')
def Details2():
    data = db.getDetailsFromDatabase("Temperature")
    lijst = []
    for Temp in data:
        lijst.append(Temp[2])
    return render_template("Details2.html", Data=lijst)


@app.route('/details3')
def Details3():
    data = db.getDetailsFromDatabase("Humidity")
    lijst = []
    for Humidity in data:
        lijst.append(Humidity[1])
    return render_template("Details3.html", Data=lijst)


@app.route('/details4')
def Details4():
    data = db.getDetailsFromDatabase("Humidity")
    lijst = []
    for Humidity in data:
        lijst.append(Humidity[2])
    return render_template("Details4.html", Data=lijst)


@app.route('/over')
def Over():
    return render_template("Over.html")


@app.route('/instellingen')
def instellingen():
    data = db.getOneSingleRowData("Settings")
    return render_template('instellingen.html', Data=data)


@app.route('/setInstellingen', methods=['POST'])
def setInstellingen():
    Temp = 0
    Hum = 0
    settings = db.getOneSingleRowData("Settings")
    for setting in settings:
        Temp = setting[1]
        Hum = setting[2]

    try:
        Temperature = request.form['Temperature']
        if Temperature == "":
            Temperature = Temp
        Humidity = request.form['Humidity']
        if Humidity == "":
            Humidity = Hum

        db.SettingsToDatabase(int(Temperature), int(Humidity))
        print(Temperature, Humidity)
    except:
        print("error in wegschrijven of ingava")

    return redirect('/instellingen')


@app.route('/truncate')
def truncate():
    db.truncate_table("Temperature")
    db.truncate_table("Humidity")
    return redirect("/")


@app.route('/shutdown', methods=['GET'])
def shutdown():
    t.do_run = False
    t.join()
    t2.do_run = False
    t2.join()
    GPIO.output(Rled, GPIO.LOW)
    GPIO.output(Gled, GPIO.LOW)
    GPIO.output(Bled, GPIO.LOW)
    GPIO.output(pump, GPIO.LOW)
    GPIO.output(fan, GPIO.LOW)
    LCD.lcd_clear(False)
    GPIO.cleanup()
    servo.stopServo()
    shutdown_server()
    return render_template("shutdown.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', use_reloader=False, threaded=True)
