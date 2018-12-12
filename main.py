# Classes
from session import OnboardingSession
from socketio import SocketCom
from mrtd import MRTD
# Helpers
import zenroom_buffer
import image_handler
from ocr import OCR
# Config
import config
# Core
import os, json, time, logging, sys, getopt
from threading import Event, Thread

class Main:
    def __init__(self, api_url):
        self.api_url = api_url
        self.session = None
        self.ready = None
        self.socket_com = None
        self.encryption_script = None
        
        self.ocr = OCR()

        self.mrz = None
        self.mrtd_data = None
        self.public_key = None
        self.encrypted_data = None

        self.i = 0

    def start(self):
        """
        1) Setup session & import Zencode script
        """
        api_url = self.api_url
        logging.info("Connecting with: {}".format(api_url))
        self.session = OnboardingSession(api_url)

        self.ready = Event()
        self.socket_com = SocketCom(self.ready, api_url)
        self.socket_com.join_room(self.session.session_id)

        with open('zenroom/encrypt_message.lua', 'r') as input:
            self.encryption_script = input.read()
        
        # self.get_mrz()
                
    def get_mrz(self):
        """
        2) Get MRZ from ID document, should become OCR
        """
        self.mrz = config.MRZ_CONFIG['mrz1']

        # self.mrz = self.ocr.get_mrz()
        # if self.mrz:
        #     return True
        
    def setup_mrtd(self):
        """
        3) Setup MRTD and get data
        """
        output_file = False
        id_card = MRTD(self.mrz, output_file)
        
        personal_data = id_card.personal_data()

        if personal_data == None:
            logging.error("DG1 could not be read")
            return False

        image_base64 = id_card.photo_data()

        if image_base64 == None:
            logging.error("DG2 could not be read")
            return False

        self.mrtd_data = [ {'personal_data': personal_data}, {'image_base64': image_base64} ]

    def test_loop(self):
        self.i += 1

        if self.i is 5:
            return True

    def show_qr(self):
        """
        4) Show QR code with session ID
        """
        logging.info("Displaying QR code & waiting session status update")
        image_handler.qr_image(self.session.session_id)

        self.ready.wait()

    def get_pkey(self):
        """
        5) Retrieve public key from session
        """
        session_data = self.session.get_data()
        p_key = session_data['data']['public_key']
        self.public_key = {'public': p_key}

    def encrypt_data(self):
        """
        6) Encrypt data with public key
        """
        # for test purposes
        self._save_data(self.mrtd_data)

        self.encrypted_data = zenroom_buffer.execute(self.encryption_script, json.dumps(self.public_key), json.dumps(self.mrtd_data))

    def _save_data(self, data):
        """
        6.2) Save encrypted data for testing purposes
        """
        with open('output/test_data.json', 'w') as output:
            json.dump(data, output)

    def attach_data(self):
        """
        7) Add encrypted data to session
        """
        self.session.attach_encrypted_data(self.encrypted_data)


logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

# print(str(sys.argv))

api_url = config.SERVER_CONFIG['prod']

arg = str(sys.argv)[13:][:5]
if arg == "--dev":
    api_url = config.SERVER_CONFIG['dev']

main = Main(api_url)

main.start()
main.get_mrz()
main.setup_mrtd()
# main.show_qr()
# main.get_pkey()
# main.encrypt_data()
# main.attach_data()