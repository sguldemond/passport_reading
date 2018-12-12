# Classes
from session import OnboardingSession
from socketio import SocketCom
from mrtd import MRTD
# Helpers
import zenroom_buffer
import image_handler
import ocr
# Config
import config
# Core
import os, json, time, logging, sys, getopt
from threading import Event

class Main:
    def start(self, api_url):
        """
        1) Setup session & import Zencode script
        """
        # api_url = config.SERVER_CONFIG['api_url']
        logging.info("Connecting with: {}".format(api_url))
        self.session = OnboardingSession(api_url)

        self.ready = Event()
        self.socket_com = SocketCom(self.ready, api_url)
        self.socket_com.join_room(self.session.session_id)

        with open('zenroom/encrypt_message.lua', 'r') as input:
            self.encryption_script = input.read()
        
        mrz = self._get_mrz()
        mrtd_data = self._setup_mrtd(mrz)
        qr_read = self._show_qr()
        p_key = self._get_pkey()
        encrypted_data = self._encrypt_data(mrtd_data, p_key)
        data_attached = self._attach_data(encrypted_data)

    def _get_mrz(self):
        """
        2) Get MRZ from ID document, should become OCR
        """
        return config.MRZ_CONFIG['mrz1']

        # logging.info("Reading MRZ with OCR...")
        # mrz = ocr.get_mrz()
        # logging.info("MRZ read [{}]".format(mrz))
        # return mrz

    def _setup_mrtd(self, mrz):
        """
        3) Setup MRTD and get data
        """
        id_card = MRTD(mrz, True)
        
        personal_data = id_card.personal_data()

        if personal_data == None:
            logging.error("DG1 could not be read, starting over...")
            self.start()

        image_base64 = id_card.photo_data()

        if image_base64 == None:
            logging.error("DG2 could not be read, starting over...")
            self.start()


        return [ {'personal_data': personal_data}, {'image_base64': image_base64} ]

    def _show_qr(self):
        """
        4) Show QR code with session ID
        """
        logging.info("Displaying QR code & waiting session status update")
        image_handler.qr_image(self.session.session_id)

        self.ready.wait()
        return True

    def _get_pkey(self):
        """
        5) Retrieve public key from session
        """
        session_data = self.session.get_data()
        public_key = session_data['data']['public_key']
        external_public_key = {'public': public_key}

        return external_public_key

    def _encrypt_data(self, data, public_key):
        """
        6) Encrypt data with public key
        """
        # for test purposes
        # self._save_data(data_to_encrypt)

        encrypted_data = zenroom_buffer.execute(self.encryption_script, json.dumps(public_key), json.dumps(data))

        return encrypted_data
        
    def _save_data(self, data):
        """
        6.2) Save encrypted data for testing purposes
        """
        with open('output/test_data.json', 'w') as output:
            json.dump(data, output)

    def _attach_data(self, data):
        """
        7) Add encrypted data to session
        """
        self.session.attach_encrypted_data(data)
        
        return True


logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

# print(str(sys.argv))

api_url = config.SERVER_CONFIG['prod']

arg = str(sys.argv)[13:][:5]
if arg == "--dev":
    api_url = config.SERVER_CONFIG['dev']

main = Main()
main.start(api_url)
