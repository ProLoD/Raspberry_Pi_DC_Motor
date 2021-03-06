import RPi.GPIO as GPIO
import time
import requests

OUTPUT_PIN_LEFT = 15
OUTPUT_PIN_RIGHT = 18
REQUEST_URL = "https://utev.org/Data?q=move"
# INTERVAL_MS = 0
FORWARD_DURATION = 1
TURN_DURATION = 1

start_time = -1
current_time = -1

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(OUTPUT_PIN_LEFT, GPIO.OUT)
    GPIO.setup(OUTPUT_PIN_RIGHT, GPIO.OUT)

def make_request():
    r = requests.get(REQUEST_URL)
    json_data = r.json()
    commands = json_data['sequence']
    return commands

def drive_forward():
    start_time = time.time()
    current_time = time.time()
    GPIO.output(OUTPUT_PIN_LEFT, GPIO.HIGH)
    GPIO.output(OUTPUT_PIN_RIGHT, GPIO.HIGH)
    while current_time <= start_time + FORWARD_DURATION:
        current_time = time.time()
    GPIO.output(OUTPUT_PIN_LEFT, GPIO.LOW)
    GPIO.output(OUTPUT_PIN_RIGHT, GPIO.LOW)

def turn_left():
    start_time = time.time()
    current_time = time.time()
    GPIO.output(OUTPUT_PIN_RIGHT, GPIO.HIGH)
    while current_time <= start_time + TURN_DURATION:
        current_time = time.time()
    GPIO.output(OUTPUT_PIN_RIGHT, GPIO.LOW)

def turn_right():
    start_time = time.time()
    current_time = time.time()
    GPIO.output(OUTPUT_PIN_LEFT, GPIO.HIGH)
    while current_time <= start_time + TURN_DURATION:
        current_time = time.time()
    GPIO.output(OUTPUT_PIN_LEFT, GPIO.LOW)

def execute(commands):
    for command in commands.split(','):
        if command == "forward":
            print("go forward")
            drive_forward()
        elif command == "left":
            print("turn left")
            turn_left()
        elif command == "right":
            print("turn left")
            turn_right()
        elif command == "stay":
            print("stay")


if __name__ == "__main__":
    setup()
    try:
        print("start")
        while True:
            commands = make_request()
            execute(commands)
            time.sleep(1)
        print("end")
    finally:
        print("cleanup")
        GPIO.cleanup()
