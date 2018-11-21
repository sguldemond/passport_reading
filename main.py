# Classes
from session import OnboardingSession, SocketCom
from mrtd import MRTD
# Helpers
import zenroom_buffer
import image_handler
# Core
import os, json, time

class Main():
    def __init__(self, api_url):
        self.api_url = api_url

    def start(self):
        """
        1) Setup session & import Zencode script
        """
        self.session = OnboardingSession(self.api_url)
        # self.socket_com = SocketCom(api_url)
        # self.socket_com.join_room(self.session.session_id)

        with open('zenroom/encrypt_message.lua', 'r') as input:
            self.encryption_script = input.read()
        
        self._get_mrz()
        self._show_qr()

    def _get_mrz(self):
        """
        2) Get MRZ from ID document, should become OCR
        """
        with open('config.json') as input:
            json_input = json.load(input)
            mrz_string = json_input['mrz']
        
        self._setup_mrtd(mrz_string)

    def _setup_mrtd(self, mrz_string):
        """
        3) Setup MRTD and get data
        """
        id_card = MRTD(mrz_string)
        self.personal_data = id_card.personal_data()
        self.image_base64 = id_card.photo_data()

    def _show_qr(self):
        """
        4) Show QR code with session ID
        """
        image_handler.qr_image(self.session.session_id)

        waiting = True
        while waiting:
            if self.session.socket_com.session_status == 'CONTINUED_1':
                waiting = False
        
        self._get_pkey()

    def _get_pkey(self):
        """
        5) Retrieve public key from session
        """
        session_data = self.session.get_data()
        public_key = session_data['data']['public_key']
        external_public_key = {'public': public_key}

        self._encrypt_data(external_public_key)

    def _encrypt_data(self, public_key):
        """
        6) Encrypt data with public key
        """
        data_to_encrypt = []
        data_to_encrypt.append({'personal_data': self.personal_data})
        data_to_encrypt.append({'image_base64': self.image_base64})

        # for test purposes
        self._save_data(data_to_encrypt)

        data = zenroom_buffer.execute(self.encryption_script, json.dumps(public_key), json.dumps(data_to_encrypt))
        
        self._attach_data(data)

    def _save_data(self, data):
        """
        6.2) Save encrypted data for testing purposes
        """
        with open('zenroom/test_data.json', 'w') as output:
            json.dump(data, output)

    def _attach_data(self, data):
        """
        7) Add encrypted data to session
        """
        self.session.attach_encrypted_data(data)
        
        print("Done, closing!")


main = Main("http://127.0.0.1:5000")
main.start()