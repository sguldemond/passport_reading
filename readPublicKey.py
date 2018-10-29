from pypassport.epassport import EPassport, mrz
from pypassport.reader import ReaderManager, PcscReader
import json

rm = ReaderManager()
print "Waiting for card..."
reader = rm.waitForCard()

with open('mrz.json') as input:
    json_input = json.load(input)
    mrz_idcard = json_input['id_card']
    mrz_passport = json_input['passport']

epassport = EPassport(reader, mrz_passport)

epassport.setCSCADirectory('resources/certificates')
# certificate = epassport.getCertificate()
# # print(certificate)

verify_certificate = epassport.doVerifySODCertificate()
print(verify_certificate)


# dg15 = epassport['DG15']
# print(dg15)

# public_key = epassport.getPublicKey()
# print(public_key)

# aa_result = epassport.doActiveAuthentication()
# print(aa_result)