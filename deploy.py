from fabric import Connection


PI_URL = 'pi@192.168.100.100'
APP_FOLDER = '/home/pi/clockApi'

c = Connection(PI_URL)


c.run('curl -X POST http://0.0.0.0:5000/shutdown', warn=True)
c.run('cd {} && git pull -r'.format(APP_FOLDER))

prefix = 'cd {} && source env/bin/activate'.format(APP_FOLDER)
c.run('{} && pip install -r requirements.txt'.format(prefix))
c.run('{} && python app.py &'.format(prefix))
