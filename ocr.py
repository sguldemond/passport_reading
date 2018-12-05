from passporteye import read_mrz
from passporteye.mrz.text import MRZCheckDigit
from PIL import Image
import cv2

import os, time, io, re
"""
TODO:
- document mambojumbo
"""
def get_mrz():
    cap = cv2.VideoCapture(0)
    tmp_file = 'tmp_capture.png'
    mrz_list = None
    
    while(True):
        _, frame = cap.read()
        cv2.imwrite(tmp_file, frame)
        mrz = read_mrz(tmp_file)
        print("Trying...")
        if mrz != None:
            mrz_list = [mrz.number, mrz.date_of_birth, mrz.expiration_date]
            print(mrz_list)

            valid_number = validate_doc_number(mrz.number, mrz.check_number)
            if (valid_number != None) & mrz.valid_date_of_birth & mrz.valid_expiration_date:
                mrz_list = [valid_number, mrz.date_of_birth, mrz.expiration_date]
                print(mrz_list)
                break
        
        time.sleep(.5)

    cap.release()
    cv2.destroyAllWindows()
    os.remove(tmp_file)
    return mrz_list

def validate_doc_number(number, check_number):
    for number in permutations(number):
        computed_check_number = MRZCheckDigit.compute(number)
        # print(check_number, computed_check_number)
        if check_number == computed_check_number:
            return number
    
    return None

def permutations(s, before="", replace="O", replace_by="0"):
    if len(s) == len(before):
       result = []
    elif replace in s[len(before):]:
       pattern = r'(^{before}[^{replace}]*)({replace})(.*$)'.format(before=before, replace=replace)
       replaced = re.sub(pattern, r'\1[]\3', s).replace("[]", replace_by)
       result = [s, replaced]
       before = re.sub(pattern, r'\1', s)
       result.extend(permutations(s, before + replace, replace, replace_by))
       result.extend(permutations(replaced, before + replace_by, replace, replace_by))
    else:
       result = [s]
    return result

# print(permutations(""))
# print(permutations("aObOcOd", "", "b", "XYZ"))
# print(permutations("NOHFO7F71"))

# get_mrz()