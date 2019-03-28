import time
from datetime import datetime

from flask import Flask, send_file
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

PLAYERS = ['BLACK', 'WHITE']


def take_photo(filename):
    from picamera import PiCamera
    with PiCamera() as camera:
        camera.resolution = (256, 256)
        camera.start_preview()
        time.sleep(0.5)  # Camera warm-up time
        camera.capture(filename)


class Clock(Resource):
    CLOCK_TOUCHER = 0

    def get(self):
        # initialize the camera and grab a reference to the raw camera capture
        filename = '/home/pi/pics/'
        filename += datetime.now().strftime("%Y%m%d_%H%M%S%f")
        filename += "_{player}.png".format(player=PLAYERS[self.CLOCK_TOUCHER])
        take_photo(filename)
        self.CLOCK_TOUCHER = 1 - self.CLOCK_TOUCHER
        return send_file(filename, mimetype='image/png')


api.add_resource(Clock, '/clock')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
