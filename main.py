# Classes
from session import OnboardingSession, SocketCom
from mrtd import MRTD
# Helpers
import zenroom_buffer
import image_handler
# Core
import os, json, time

class Main():

    # 1) Setup session & import Zencode script
    def start(self):
        api_url = "http://127.0.0.1:5000"
        self.session = OnboardingSession(api_url)

        self.socket_com = SocketCom(self, api_url)
        self.socket_com.join_room(self.session.session_id)

        with open('zenroom/encrypt_message.lua', 'r') as input:
            self.encryption_script = input.read()
        
        self.get_mrz()
        self.show_qr()

    # 2) Get MRZ from ID document, should become OCR
    def get_mrz(self):
        with open('config.json') as input:
            json_input = json.load(input)
            mrz_string = json_input['mrz']
        
        self.setup_mrtd(mrz_string)

    # 3) Setup MRTD and get data
    def setup_mrtd(self, mrz_string):
        id_card = MRTD(mrz_string, False)
        self.personal_data = id_card.personal_data()
        self.image_base64 = id_card.photo_data()

    # 4) Show QR code with session ID
    def show_qr(self):
        image_handler.qr_image(self.session.session_id)

        while True:
            if self.socket_com.session_status is 'CONTINUED_1':
                self.get_pkey()                

    # 5) Wait for user to connect
    def wait_for_user():
        print "Waiting for user to connect with session..."
        wait_for_client = True
        last_status = session.get_status()
        print "Latest session status: {}".format(last_status)
        while wait_for_client:        
            status = session.get_status()
            if status != last_status:
                print "Latest session status: {}".format(status)
                last_status = status

            if status == 'CONTINUED_1':
                wait_for_client = False
            
            time.sleep(2)

        print "User connected to session, continuing"

    # 6) Retrieve public key from session
    def get_pkey(self):
        session_data = self.session.get_data()
        public_key = session_data['data']['public_key']
        external_public_key = {'public': public_key}

        self.encrypt_data(external_public_key)

    # 7.1) Encrypt data with public key
    def encrypt_data(self, public_key):
        data_to_encrypt = []
        data_to_encrypt.append({'personal_data': self.personal_data})
        data_to_encrypt.append({'image_base64': self.image_base64})

        # for test purposes
        self.save_data(data_to_encrypt)

        data = zenroom_buffer.execute(self.encryption_script, json.dumps(public_key), json.dumps(data_to_encrypt))
        
        self.attach_data(data)

    # 7.2) Save encrypted data for testing purposes
    def save_data(data):
        with open('zenroom/test_data.json', 'w') as output:
            json.dump(data, output)

    # 8) Add encrypted data to session
    def attach_data(self, data):
        self.session.attach_encrypted_data(data)

main = Main()
main.start()