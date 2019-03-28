import time
from datetime import datetime

from flask import Flask, send_file
from flask_restful import Resource, Api
from picamera import PiCamera

app = Flask(__name__)
api = Api(app)

PLAYERS = ['BLACK', 'WHITE']
CLOCK_TOUCHER = 0


class Clock(Resource):
    def get(self):
        # initialize the camera and grab a reference to the raw camera capture
        filename = '/home/pi/pics/'
        filename += datetime.now().strftime("%Y%m%d_%H%M%S%f")
        filename += "_{player}.png".format(player=PLAYERS[CLOCK_TOUCHER])
        with PiCamera() as camera:
            camera.resolution = (256, 256)
            camera.start_preview()
            time.sleep(0.5)  # Camera warm-up time
            camera.capture(filename)
        global CLOCK_TOUCHER
        CLOCK_TOUCHER = 1 - CLOCK_TOUCHER
        return send_file(filename, mimetype='image/png')

api.add_resource(Clock, '/clock')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
