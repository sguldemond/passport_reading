# pypassport
from pypassport.reader import ReaderManager
from pypassport.epassport import EPassport, mrz
from pypassport.doc9303 import tagconverter

# local
from image_handler import convert_image

import json

class Passport:
    def __init__(self, mrz, reader_type="ACR1252U", output=False):
        self.mrz_string = mrz
        self.reader_type = reader_type
        self.output = output
        self.reader_obj = None
    
    def _set_reader_obj(self):
        if self.reader_obj != None:
            return
        
        rm = ReaderManager()
        print "Waiting for card..."
        self.reader_obj = rm.waitForCard()
    
    def _check_mrz(self):
        mrz_obj = mrz.MRZ(self.mrz_string)
        return mrz_obj.checkMRZ()
    
    def _set_epassport(self):
        if self._check_mrz() == False:
            print "MRZ is not valid"
            return False
        
        self._set_reader_obj()

        self.epassport = EPassport(self.reader_obj, self.mrz_string)
        return True

    def personal_data(self):
        self._set_epassport()

        # if self._set_epassport() == False:
        #     print "EPassport not set"
        #     return
        
        dg1_data = self.epassport['DG1']

        clean_info = {}
        for attribute, value in dg1_data.iteritems():
            tag_name = tagconverter.tagToName[attribute]
            clean_info.update({tag_name: value})
        
        if self.output:
            doc_number_tag = '5A'
            doc_number = dg1_data[doc_number_tag]

            with open('output/' + doc_number + '.json', 'w') as outfile:
                json.dump(clean_info, outfile)

        return clean_info

    def image(self):
        if self._set_epassport() == False:
            print "EPassport not set"
            return

        dg2_data = self.epassport['DG2']

        # check from ePassportviewer
        if dg2_data['A1'].has_key('5F2E'): tag = '5F2E' # 5F2E: Biometric data block 
        elif dg2_data['A1'].has_key('7F2E'): tag = '7F2E' # 7F2E: Biometric data block (enciphered) 

        img_data = dg2_data['A1'][tag]

        if self.output:
            dg1_data = self.epassport['DG1']
            doc_number_tag = '5A'
            output_name = dg1_data[doc_number_tag]
        else:
            output_name = "tmp"

        return convert_image(img_data, output_name, self.output)