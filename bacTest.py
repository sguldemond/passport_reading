from pypassport.epassport import EPassport, mrz
from pypassport.reader import ReaderManager, PcscReader

rm = ReaderManager()

print "Waiting for card..."
reader = rm.waitForCard()
print(reader)

m2 = 'NXHF07F750NLD9109032M2510262207074392<<<<<68'
mrz_obj = mrz.MRZ(m2)
mrz_obj.checkMRZ()

epassport = EPassport(reader, m1)

rnd_icc = "57516B00CC49A1199000"
cmd_data = epassport._bac.authentication(rnd_icc)

print(cmd_data)