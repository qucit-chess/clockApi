from fabric import Connection


PI_URL = 'pi@192.168.100.100'


c = Connection(PI_URL)
c.run('curl -X POST http://0.0.0.0:5000/shutdown')
c.run('/home/pi/clockApi')
c.run('git pull -r')
c.run('source env/bin/activate')
c.run('python app.py')
