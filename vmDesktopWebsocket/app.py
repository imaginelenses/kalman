from flask import Flask
from flask.templating import render_template
from flask_socketio import SocketIO

import eventlet
eventlet.monkey_patch()


app = Flask(__name__)

socket = SocketIO(app, async_mode='eventlet', cors_allowed_origins = "*")

@socket.on('move_event', namespace='/')
def move(x, y, z, timestamp):
    """ Your code goes here """
    print(x, y, z, timestamp)



@socket.on('connect', namespace='/')
def open():
    print('Connected')

@socket.on('disconnect', namespace='/')
def close():
    print('Disconnected')

def serve():
    socket.run(app, host='192.168.0.149', port='8080', debug=True, use_reloader=False)
    

if __name__ == '__main__':
    serve()
    
