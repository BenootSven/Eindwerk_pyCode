from flask import Flask, render_template, request, redirect
from Klassen.I2CLCDklasse import i2cLCD
from Klassen.MCPklasse import SPI
from Klassen.ServoEindwerkKlasse import Servo
from Klassen.OneWireSensorKlasse import OneWireSensor
from threading import Thread
from flask_socketio import SocketIO
from gevent import monkey
import RPi.GPIO as GPIO
import time

monkey.patch_all()

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

# LCD = i2cLCD(0x27, 16)
# LCD.lcd_init()
#
# MCP = SPI()
#
# onewire1 = OneWireSensor('/sys/bus/w1/devices/28-000008c5ac92/w1_slave')
# onewire2 = OneWireSensor('/sys/bus/w1/devices/28-000008e097d8/w1_slave')

app = Flask(__name__)
socketio = SocketIO(app)
thread = None


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def background_program():
    while True:
        time.sleep(1)
        print("Background task!")


@app.route('/')
def Home():
    # global thread
    # if thread is None:
    #     thread = Thread(target=background_program)
    #     thread.start()
    return render_template("Home.html")


@app.route('/details')
def Details():
    return render_template("Details.html")


@app.route('/details2')
def Details2():
    return render_template("Details2.html")


@app.route('/details3')
def Details3():
    return render_template("Details3.html")


@app.route('/details4')
def Details4():
    return render_template("Details4.html")


@app.route('/over')
def Over():
    return render_template("Over.html")

@app.route('/test')
def test():
    return render_template("test.html")


@app.route('/set', methods=['POST'])
def handle_data():
    tekst = request.form['value_set']
    print(tekst)

    # if tekst == "11":
    #     LCD.lcd_clear()
    #     LCD.lcd_string("Last update:", 0)
    #     LCD.lcd_string("pomp aan", 1)
    #     GPIO.output(pump, GPIO.HIGH)
    #
    # if tekst == "10":
    #     LCD.lcd_clear()
    #     LCD.lcd_string("Last update:", 0)
    #     LCD.lcd_string("pomp uit", 1)
    #     GPIO.output(pump, GPIO.LOW)
    #
    # if tekst == "21":
    #     LCD.lcd_clear()
    #     LCD.lcd_string("Last update:", 0)
    #     LCD.lcd_string("ventilator aan", 1)
    #     GPIO.output(fan, GPIO.HIGH)
    #
    # if tekst == "20":
    #     LCD.lcd_clear()
    #     LCD.lcd_string("Last update:", 0)
    #     LCD.lcd_string("ventilator uit", 1)
    #     GPIO.output(fan, GPIO.LOW)
    #
    # if tekst == "31":
    #     LCD.lcd_clear()
    #     LCD.lcd_string("Last update:", 0)
    #     LCD.lcd_string("LED aan", 1)
    #     GPIO.output(Rled, GPIO.HIGH)
    #     GPIO.output(Gled, GPIO.HIGH)
    #     GPIO.output(Bled, GPIO.HIGH)
    #
    # if tekst == "30":
    #     LCD.lcd_clear()
    #     LCD.lcd_string("Last update:", 0)
    #     LCD.lcd_string("LED uit", 1)
    #     GPIO.output(Rled, GPIO.LOW)
    #     GPIO.output(Gled, GPIO.LOW)
    #     GPIO.output(Bled, GPIO.LOW)
    #
    # if tekst == "41":
    #     LCD.lcd_clear()
    #     servo = Servo(18, 50)
    #     servo.init()
    #     LCD.lcd_string("Last update:", 0)
    #     LCD.lcd_string("Dak open", 1)
    #     servo.servoDakOpen(0.03)
    #     servo.stopServo()
    #
    # if tekst == "40":
    #     LCD.lcd_clear()
    #     servo = Servo(18, 50)
    #     servo.init()
    #     LCD.lcd_string("Last update:", 0)
    #     LCD.lcd_string("Dak toe", 1)
    #     servo.servoDakToe(0.03)
    #     servo.stopServo()
    #
    # if tekst == "51":
    #     temp1 = onewire1.read_temp()
    #     temp2 = onewire2.read_temp()
    #     print("temperatuur binnen = %s" % temp1)
    #     print("temperatuur buiten = %s" % temp2)
    #     LCD.lcd_clear()
    #     LCD.lcd_string("binnen = " + str(temp1), 0)
    #     LCD.lcd_string("buiten = " + str(temp2), 1)
    #
    # if tekst == "61":
    #     vocht1 = (100 - (MCP.readChannel(0) / 1023) * 100)
    #     vocht2 = (100 - (MCP.readChannel(1) / 1023) * 100)
    #     print("Vochtigheid sensor1 = %s" % vocht1)
    #     print("Vochtigheid sensor2 = %s" % vocht2)
    #     LCD.lcd_clear()
    #     LCD.lcd_string("Vocht1 = %0.2f" % vocht1, 0)
    #     LCD.lcd_string("Vocht2 = %0.2f" % vocht2, 1)

    return redirect("/")


@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    GPIO.output(Rled, GPIO.LOW)
    GPIO.output(Gled, GPIO.LOW)
    GPIO.output(Bled, GPIO.LOW)
    GPIO.output(pump, GPIO.LOW)
    GPIO.output(fan, GPIO.LOW)
    # LCD.lcd_clear(False)
    GPIO.cleanup()
    return render_template("shutdown.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', use_reloader=False, threaded=True)
