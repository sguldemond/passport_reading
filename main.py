from mrtd import MRTD
import zenroom_buffer
from session import OnboardingSession

import os, json, time

### start Init Session ###
session = OnboardingSession()
print(session.session_id)
wait_for_client = True
while wait_for_client:
    status = session.get_status()
    print(status)
    if status == 'CONTINUED_1':
        wait_for_client = False
    
    time.sleep(2)
    
session_data = session.get_data()
public_key = session_data['data']['public_key']

### end Init Session ###
### start NFC Reader ###

with open('config.json') as input:
    json_input = json.load(input)
    mrz_string = json_input['mrz']

id_card = MRTD(mrz_string, True)
personal_data = id_card.personal_data()
# image_base64 = id_card.photo_data()
# print(image_base64)

### end NFC Reader ###
### start Encryption ###
with open('zenroom/encrypt_message.lua', 'r') as input:
    encryption_script = input.read()

# with open('zenroom/pub_key.keys', 'r') as input:
#     external_public_key = input.read()

external_public_key = {'public': public_key}

data_to_encrypt = []
data_to_encrypt.append({'personal_data': personal_data})
# data_to_encrypt.append({'image_base64': image_base64})

with open('zenroom/test_data.json', 'w') as output:
    json.dump(data_to_encrypt, output)

data = zenroom_buffer.execute(encryption_script, json.dumps(external_public_key), json.dumps(data_to_encrypt))
print(data)
### end Encryption ###

session.attach_encrypted_data(data)