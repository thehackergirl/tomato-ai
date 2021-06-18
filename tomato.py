from werkzeug.wrappers import Request
import RPi.GPIO as GPIO
import schedule
import threading
import time
from flask import Flask, redirect, render_template, request
# from guizero import App, TextBox


app = Flask(__name__)

print("starting jagodas tomato server")

# set the gpio in mode broadcom - so we
#  can control leds, etc
GPIO.setmode(GPIO.BCM)
# disable warnings
GPIO.setwarnings(False)

# set pin number 17 to output - so that we can use it to turn something on / off
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.HIGH)

# This function turns the valve on and off.
def valveOnOff():
    GPIO.output(17, GPIO.LOW)
    print("GPIO LOW (on), valve should be open")
    time.sleep(90)
    GPIO.output(17, GPIO.HIGH)
    print("GPIO HIGH (off), valve should be closed")

def valveOnOnly():
    GPIO.output(17, GPIO.LOW)
    print("GPIO LOW (on), valve should be open")
    
def valveOffOnly():
    GPIO.output(17, GPIO.HIGH)
    print("GPIO HIGH (off), valve should be closed")

def test():
    print('test this')


# valveOnOff()

schedule.every().day.at("07:11").do(valveOnOff)
# schedule.every().day.at("04:27").do(job)
# schedule.every(5).seconds.do(valveOnOff)


@app.route("/")
def index():
    # only return html here, use javascript call to /on and /off
    return render_template('index.html')

@app.route("/on")
def waterOn():
    valveOnOnly()
    return "{status:ok}"

# the api, important to be before loop
@app.route("/off")
def waterOff():
    valveOffOnly()
    return "{status:ok}"

@app.route('/schedule', methods=['GET'])
def schedule_function():
    text_seconds = request.args.get['text_name']
    processed_text = text_seconds.upper()
    textbox_time = request.args.get['time']
    print(processed_text)
    return processed_text

# my_form_post()
class BackgroundTasks(threading.Thread):
    def run(self,*args,**kwargs):
        app.run(host='0.0.0.0')

t = BackgroundTasks()
t.start()

# main loop of program
while True:
    print ("still running program")
    schedule.run_pending()
    time.sleep(1)

if __name__ == '__main__':
    app.debug = True
    app.run()

def api_response():
    from flask import jsonify
    if request.method == 'POST':
        return jsonify(**request.json)

GPIO.cleanup()