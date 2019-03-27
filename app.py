import time
from datetime import datetime

from flask import Flask
from picamera import PiCamera

app = Flask(__name__)

PLAYERS = ['BLACK', 'WHITE']
CLOCK_TOUCHER = 0


@app.route('/clock')
def clock():
    # initialize the camera and grab a reference to the raw camera capture
    filename = datetime.now().strftime("%Y%m%d" f'_{PLAYERS[CLOCK_TOUCHER]}_.png')
    with PiCamera() as camera:
        camera.resolution = (2592, 1944)
        camera.start_preview()
        time.sleep(0.5)  # Camera warm-up time
        camera.capture(filename)
    global CLOCK_TOUCHER
    CLOCK_TOUCHER = 1 - CLOCK_TOUCHER



if __name__ == '__main__':
    app.run()