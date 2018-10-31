from pypassport.epassport import EPassport, mrz
from pypassport.reader import ReaderManager, PcscReader
from pypassport.doc9303 import tagconverter

from image_handler import convert_image
import zenroom_pipe
import zenroom_buffer
from passport import Passport

import os, json

with open('config.json') as input:
    json_input = json.load(input)
    mrz_string = json_input['mrz']

id_card = Passport(mrz_string, True)
personal_data = id_card.personal_data()
image_base64 = id_card.image()
# print(image_base64)

### Encryption ###
with open('zenroom/encrypt_message.lua', 'r') as input:
    encryption_script = input.read()

with open('zenroom/pub_key.keys', 'r') as input:
    external_pub_key = input.read()

data_to_encrypt = personal_data

# data = zenroom_pipe.execute(encryption_script, external_pub_key, json.dumps(clean_info, ensure_ascii=False))
data = zenroom_buffer.execute(encryption_script, external_pub_key, json.dumps(data_to_encrypt))

print(data)
###