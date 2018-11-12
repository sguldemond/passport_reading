from mrtd import MRTD
# import zenroom_pipe
import zenroom_buffer

import os, json

with open('config.json') as input:
    json_input = json.load(input)
    mrz_string = json_input['mrz']

id_card = MRTD(mrz_string, True)
personal_data = id_card.personal_data()
# image_base64 = id_card.photo_data()
# print(image_base64)

### Encryption ###
with open('zenroom/encrypt_message.lua', 'r') as input:
    encryption_script = input.read()

with open('zenroom/pub_key.keys', 'r') as input:
    external_pub_key = input.read()

data_to_encrypt = []
data_to_encrypt.append({'personal_data': personal_data})
# data_to_encrypt.append({'image_base64': image_base64})



with open('zenroom/test_data.json', 'w') as output:
    json.dump(data_to_encrypt, output)

# data = zenroom_pipe.execute(encryption_script, external_pub_key, json.dumps(clean_info, ensure_ascii=False))
data = zenroom_buffer.execute(encryption_script, external_pub_key, json.dumps(data_to_encrypt))

# print(data)
###

print("Done!")