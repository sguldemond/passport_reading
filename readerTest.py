from pypassport.epassport import EPassport, mrz
from pypassport.reader import ReaderManager, PcscReader
from pypassport.openssl import OpenSSLException

rm = ReaderManager()
print(rm.getReaderList())

reader = rm.waitForCard()

print(reader)

m1 = 'I<NLDIVPRB05R24119776170<<<<<36208107M2406237NLD<<<<<<<<<<<2'
m2 = 'NXHF07F750NLD9109032M2510262207074392<<<<<68'

mrz_obj = mrz.MRZ(m2)

print(mrz_obj.checkMRZ()) 

p = EPassport(reader, m1)

x = p.readPassport()
print(x)