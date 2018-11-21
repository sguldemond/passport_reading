from session import SocketSession
import time

socket_session = SocketSession('localhost:5000')
socket_session.init_onboarding()



# keeping main thread alive in order to run SocketThread in daemon mode, so exiting is normal
while True:
    time.sleep(1)