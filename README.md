# Passport reading

## Run

There must be a file present named `mrz.json` containing the MRZ of the document thats on the scanner.
Also a folder named `output` must be present.

```
$ python reader.py
```

## Testing scanner

The scanner we're using is the [ACS ACR1252U-M1](https://www.acs.com.hk/en/products/342/acr1252u-usb-nfc-reader-iii-nfc-forum-certified-reader/), supported by the [CCID driver](https://ccid.apdu.fr/). All done on an Ubuntu 18.04 machine.

List all USB devices: `$ lsusb`

Using the [PCSC-lite](https://pcsclite.apdu.fr/) daemon `pcscd` you can check if the driver is compatible with a NFC scanner:
`$ sudo pcscd -f -d`

Start PCSC in the background:
`$ service pcscd start`

Using [pcsc-tools](http://ludovic.rousseau.free.fr/softwares/pcsc-tools/) chips on the scanner can be read, PCSC needs te be started for this:
`$ pcsc_scan`

## Available projects

### ePassportViewer
- [Origin](https://github.com/andrew867/epassportviewer)
- [GitHub mirror](https://github.com/andrew867/epassportviewer)

It is supported by the pypassport python library, which can be found in the same repository.

These projects have been actively investigated. It takes some time to get all the needed software installed since main project was last updated 4 years ago. But the viewer and pypassport library are working.
We got stuck at reading the passport information.

To experiment with changes in the pypassport library you need to reinstall it every time.
This is done inside a virtual environment.

#### Changes made so far

Changing protocol from T0 to T1, based on experiments done using [gscriptor](ludovic.rousseau.free.fr/softwares/pcsc-tools/)
```
# self._pcsc_connection.connect(self.sc.scard.SCARD_PCI_T0)
self._pcsc_connection.connect(self.sc.scard.SCARD_PCI_T1)
```
pypassport > reader.py > class PcscReader > def connect: 

Adding this line,
```
mrz = self._mrz
```
to pypassport > doc9303 > mrz.py > class MRZ > def _checkDigitsTD1 & def _checkDigitsTD2

When running the 'EPassport.readPassport' method we came across an error with this message:
```
('Data not found:', '6F63')
```
This is most likely a merging of the '6F' and '63' which are the locations of DG15 (Public Keys) and DG3 (Finger Print) respectively on the LDS (Logical Data Structure). For some reason these two tags are stored conjoined in the common file, which contains a list of available DG's. This list can be read using 'EPassport.readCom'.

I added this code to 'readCom', which does not yet fix the whole problem:
```
# Temp fix for 6F63 Data not found issue
double_tag = False
ef_com = self["Common"]["5C"]
for tag in ef_com:
  if tag == "6F63":
  ef_com.append("6F")
  ef_com.append("63")
  double_tag = True
        
  if double_tag:
  ef_com.remove("6F63")
        
 # print(ef_com)
 ###
```

For some reason DG15 returns empty and for DG3 the 'securty status is not satisfied'.
For now this can be skipped, with the info from DG15 (public keys) the info on the NFC can be varified as valid, but this is not relevant for us at this moment. We also don't need DG3 (Finger Print).

#### Processing face image

The face image is located in DG2 (DG is short for Data Group), corrosponding with tag '75', more info about this can be found at ICAO Doc 9303. It is formatted in JPEG2000 (jp2), so in order to use it properly it should be converted to another format like jpg or png.

The pypassport module provides some code thats shows how to do this, but in order for this to work some libraries have to be installed first.

First install [JasPer](http://www.ece.uvic.ca/~frodo/jasper/), this is used by GraphicsMagick and handles JPEG2000 files
It is available [here](https://github.com/mdadams/jasper), but the build and install process is quite unfriendly. I ended up with the following process:

```
$ git clone https://github.com/xorgy/graphicsmagick // this is a large download, but couldn't get it working otherwise
$ cd graphicsmagick/jp2
$ export CFLAGS="-O2 -fPIC" // this is important later when installing GraphicsMagick
$ ./configure
$ make
$ sudo make install
```

Then install GraphicsMagick, image processing software, from anywhere [here](http://www.graphicsmagick.org/download.html), I used version 1.3.30.
```
$ 'Download from web & enter folder'
$ ./configure --with-modules --enable-shared=yes --disable-installed=yes // is has to be shared in order for pgmagick to use it
$ make
$ sudo make install
$ ldconfig // 'For security and performance reasons, Linux maintains a cache of the shared libraries installed in "approved" locations and this command will update it.'
```

GraphicsMagick should support JPEG2000 now, you can check this by running:
```
$ gm version
```
It should list `JPEG-2000 ... yes` under `Feature Support`.

Finally install [pgmagick](https://github.com/hhatto/pgmagick), which is a "boost.python based wrapper for GraphicsMagick" 
```
$ git clone https://github.com/hhatto/pgmagick
$ python setup.py install
```
Do not install pgmagick through `pip`, this version includes its own version of GraphicsMagick which will not support JPEG2000.

### JMRTD
> "An Open Source Java Implementation of Machine Readable Travel Documents"
- [Homepage](https://jmrtd.org/)

Used by ReadID app.
Has not been investigated yet.

## Relevant information

The standard around Machine Readable Travel Documents can be found at [ICAO Doc 9303](https://www.icao.int/publications/pages/publication.aspx?docnum=9303)
