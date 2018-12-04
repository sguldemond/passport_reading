import unittest
from mrtd import MRTD
from pypassport.reader import TimeOutException

class TestPassportClass(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestPassportClass, self).__init__(*args, **kwargs)

        self.valid_mrz = "ABCD01A236???9001011?2001012<<<<<<<<<<<<<<06"

    # Testing MRZ string creation when using list
    def test_mrz_string(self):
        mrz = ['ABCD01A23', '900101', '200101']
        passport_obj = MRTD(mrz)

        self.assertEqual(passport_obj.mrz_string, "ABCD01A236???9001011?2001012<<<<<<<<<<<<<<06")

    # Testing behavior when there is no card on the reader
    def test_wait_reader(self):
        passport_obj = MRTD(self.valid_mrz)
    
if __name__ == '__main__':
    unittest.main()
