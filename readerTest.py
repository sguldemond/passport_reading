from pypassport.epassport import EPassport, mrz
from pypassport.reader import ReaderManager, PcscReader
from pypassport.openssl import OpenSSLException

rm = ReaderManager()
print(rm.getReaderList())

# rm.waitForCard()

reader = rm.getReaderList()[1]
rm.create(reader)

print(type(reader))

print(reader)

# mrz = mrz.MRZ('NXHF07F75ONLD9109032M2510262207074392<<<<<68')
# print(mrz.checkMRZ())

# p = EPassport(mrz, reader)
# print(p["DG1"])