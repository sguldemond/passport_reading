from socketIO_client import SocketIO
import time
from threading import Thread

class SocketThread(Thread):

    def __init__(self, parent, api_url):
        Thread.__init__(self)
        self.parent = parent
        
        self.socketIO = SocketIO(api_url)
        self.socketIO.on('status_update', self.on_status_update)

    def on_status_update(self, *args):
        self.parent.on_status_update(args)

    def on_join_room_response(*args):
        print('on_join_room_response')

    def join_room(self, room):
        self.socketIO.emit('join_room', {'room': room}, self.on_join_room_response)

    def run(self):
        self.socketIO.wait()