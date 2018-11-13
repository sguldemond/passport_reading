# 0) Python imports
# Classes
from session import OnboardingSession
from mrtd import MRTD
# Helpers
import zenroom_buffer
import image_handler
# Core
import os, json, time


# 1) Setup
session = OnboardingSession("http://127.0.0.1:5000")
with open('zenroom/encrypt_message.lua', 'r') as input:
    encryption_script = input.read()


# 2) Get MRZ from ID document, should become OCR
with open('config.json') as input:
    json_input = json.load(input)
    mrz_string = json_input['mrz']


# 3) Setup MRTD and get data
id_card = MRTD(mrz_string, False)
personal_data = id_card.personal_data()
# image_base64 = id_card.photo_data()


# 4) Show QR-code with session ID
image_handler.qr_image(session.session_id)


# 5) Wait for user to connect
print "Waiting for user to connect with session..."
wait_for_client = True
last_status = session.get_status()
print "Latest session status: {0}".format(last_status)
while wait_for_client:        
    status = session.get_status()
    if status != last_status:
        print "Latest session status: {0}".format(status)
        last_status = status

    if status == 'CONTINUED_1':
        wait_for_client = False
    
    time.sleep(2)

print "User connected to session, continuing"


# 6) Retrieve public key from session
session_data = session.get_data()
public_key = session_data['data']['public_key']
external_public_key = {'public': public_key}


# 7) Encrypt data with public key
data_to_encrypt = []
data_to_encrypt.append({'personal_data': personal_data})
# data_to_encrypt.append({'image_base64': image_base64})
data = zenroom_buffer.execute(encryption_script, json.dumps(external_public_key), json.dumps(data_to_encrypt))


# 7.2) Save encrypted data for testing purposes
with open('zenroom/test_data.json', 'w') as output:
    json.dump(data_to_encrypt, output)


# 8) Add encrypted data to session
session.attach_encrypted_data(data)