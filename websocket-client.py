from socketIO_client import SocketIO, BaseNamespace


class SessionNamespace(BaseNamespace):

    def on_hello(self, *args):
        print('on_hello', args)


def on_hello():
    print('hello on client')


def on_event_1(*args):
    print('on_event_1', args)


socketio_client = SocketIO('localhost', 5000)
session_namespace = socketio_client.define(SessionNamespace, '/session')

session_namespace.emit("a message from the client")
session_namespace.emit("and another message from the client")
socketio_client.wait(seconds=1)