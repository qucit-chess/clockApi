import os
import time
from datetime import datetime

from flask import Flask, send_file, render_template, make_response, request
from flask_restful import Resource, Api
from webargs import fields
from webargs.flaskparser import use_kwargs

app = Flask(__name__)
api = Api(app)

PLAYERS = ['BLACK', 'WHITE']


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def take_photo(filename, suffix=''):
    from picamera import PiCamera
    with PiCamera() as camera:
        camera.resolution = (256, 256)
        camera.start_preview()
        time.sleep(0.1)  # Camera warm-up time
        camera.capture(filename.format(suffix=suffix))


def create_game_dir():
    now = datetime.now().strftime("%Y%m%d_%H%M%S%f/")
    dirname = "/home/pi/pics/" + now
    os.mkdir(dirname)
    return dirname


class Clock(Resource):
    clock_toucher = 0
    current_dir = '/home/pi/pics/'

    args = {
        'new_game': fields.Bool(location='query', missing=False),
    }

    @use_kwargs(args)
    def get(self, new_game):
        if new_game:
            self.clock_toucher = 0
            self.current_dir = create_game_dir()

        # initialize the camera and grab a reference to the raw camera capture
        filename = self.current_dir
        filename += datetime.now().strftime("%Y%m%d_%H%M%S%f")
        filename += "_{player}_{suffix}.png".format(player=PLAYERS[self.clock_toucher], suffix='{suffix}')
        take_photo(filename, 'a')
        take_photo(filename, 'b')
        self.clock_toucher = 1 - self.clock_toucher
        return send_file(filename, mimetype='image/png')


class Index(Resource):

    def get(self):
        return make_response(render_template('index.html'))


class Shutdown(Resource):

    def post(self):
        shutdown_server()
        return 'Server shutting down...'


api.add_resource(Clock, '/clock')
api.add_resource(Index, '/')
api.add_resource(Shutdown, '/shutdown')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
