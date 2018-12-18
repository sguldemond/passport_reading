from passporteye import read_mrz
from passporteye.mrz.text import MRZCheckDigit
from PIL import Image
import cv2

import os, time, io, re, logging
"""
TODO:
- document mambojumbo
"""

class OCR:

    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.tmp_file = 'tmp_capture.png'
        self.mrz_list = None
        self.sleep_time = .5

    def get_mrz(self):
        # logging.info("Checking for valid MRZ every {0} seconds".format(sleep_time))
        
        tmp_file = self.tmp_file
        mrz_list = self.mrz_list

        _, frame = self.cap.read()
        cv2.imwrite(tmp_file, frame)
        try:
            mrz = read_mrz(tmp_file)
        except ValueError as e:
            logging.warning(e.message)
            return None

        # print("Trying...")
        if mrz != None:
            mrz_list = [mrz.number, mrz.date_of_birth, mrz.expiration_date]
            logging.info("OCR: checking string [{}]".format(mrz_list))

            valid_number = self.validate_doc_number(mrz.number, mrz.check_number)
            if (valid_number != None) & mrz.valid_date_of_birth & mrz.valid_expiration_date:
                mrz_list = [valid_number, mrz.date_of_birth, mrz.expiration_date]
                # print(mrz_list)

                os.remove(tmp_file)

                return mrz_list

        time.sleep(self.sleep_time)

        return None

    def end_capture(self):
        self.cap.release()
        # cv2.destroyAllWindow()

    def validate_doc_number(self, number, check_number):
        for number in self.permutations(number):
            computed_check_number = MRZCheckDigit.compute(number)
            if check_number == computed_check_number:
                return number
        
        return None

    def permutations(self, s, before="", replace="O", replace_by="0"):
        """
        This function will replace every occurance of a character or string with another character or string.
        In every possible setup, e.g. 'xxx' as input, where 'y' replaces 'x' will be return ['yxx', 'xyx', 'xxy', 'yyx', 'yxy', ... ]

        Written by Jurien Vegter in order to fix an issue where the passporteye ocr mistakes '0's for 'O's
        """
        if len(s) == len(before):
            result = []
        elif replace in s[len(before):]:
            pattern = r'(^{before}[^{replace}]*)({replace})(.*$)'.format(before=before, replace=replace)
            replaced = re.sub(pattern, r'\1[]\3', s).replace("[]", replace_by)
            result = [s, replaced]
            before = re.sub(pattern, r'\1', s)
            result.extend(self.permutations(s, before + replace, replace, replace_by))
            result.extend(self.permutations(replaced, before + replace_by, replace, replace_by))
        else:
            result = [s]

        return result

# print(permutations(""))
# print(permutations("aObOcOd", "", "b", "XYZ"))
# print(permutations("NOHFO7F71"))

# get_mrz()