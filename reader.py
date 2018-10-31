from pypassport.epassport import EPassport, mrz
from pypassport.reader import ReaderManager, PcscReader
from pypassport.doc9303 import tagconverter

from image_handler import convert_image
import zenroom_pipe
import zenroom_buffer

import json
import os

rm = ReaderManager()
# print(rm.getReaderList())

print "Waiting for card..."
reader = rm.waitForCard()
# print(reader)

with open('mrz.json') as input:
    json_input = json.load(input)
    mrz_idcard = json_input['id_card']
    mrz_passport = json_input['passport']

mrz_obj = mrz.MRZ(mrz_passport)

print "Checking MRZ..."
print(mrz_obj.checkMRZ()) 

epassport = EPassport(reader, mrz_passport)

print "Reading DG1 (MRZ)..."
dg1_data = epassport['DG1']

doc_number_tag = '5A' # see https://www.icao.int/publications/Documents/9303_p10_cons_en.pdf for more info
doc_number = dg1_data[doc_number_tag]

clean_info = {}
for attribute, value in dg1_data.iteritems():
    tag_name = tagconverter.tagToName[attribute]
    clean_info.update({tag_name: value})

# print(clean_info)

with open('output/' + doc_number + '.json', 'w') as outfile:
    json.dump(clean_info, outfile)

print "Reading DG2 (Encoded Face)..."
dg2_data = epassport['DG2']

# check from ePassportviewer
if dg2_data['A1'].has_key('5F2E'): tag = '5F2E' # 5F2E: Biometric data block 
elif dg2_data['A1'].has_key('7F2E'): tag = '7F2E' # 7F2E: Biometric data block (enciphered) 

img_data = dg2_data['A1'][tag]

print "Starting conversion..."
image_string = convert_image(img_data, doc_number)

# clean_info.update({"image": image_string})
# print(clean_info)

# with open('zenroom/info.data', 'w') as outfile:
#     json.dump(clean_info, outfile)

### Encryption ###
with open('zenroom/encrypt_message.lua', 'r') as input:
    encryption_script = input.read()

with open('zenroom/pub_key.keys', 'r') as input:
    external_pub_key = input.read()

# data = zenroom_pipe.execute(encryption_script, external_pub_key, json.dumps(clean_info, ensure_ascii=False))
data = zenroom_buffer.execute(encryption_script, external_pub_key, json.dumps(clean_info))

print(data)
###