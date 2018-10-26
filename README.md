# Passport reading

## Run

There must be a file present named `mrz.json` containing the MRZ of the document thats on the scanner.
Also a folder named `output` must be present.

```
# python reader.py
```

## Testing scanner

The scanner we're using the [ACS ACR1252U-M1](https://www.acs.com.hk/en/products/342/acr1252u-usb-nfc-reader-iii-nfc-forum-certified-reader/) scanner, supported by the [CCID driver](https://ccid.apdu.fr/). All done on a Ubuntu machine.

List all USB devices:
`# lsusb`

Using the [PCSC-lite](https://pcsclite.apdu.fr/) daemon `pcscd` you can check if the driver is compatible with a NFC scanner:
`# sudo pcscd -f -d`

Start PCSC in the background:
`# service pcscd start`

Using [pcsc-tools](http://ludovic.rousseau.free.fr/softwares/pcsc-tools/) chips on the scanner can be read, PCSC needs te be started for this:
`# pcsc_scan`

## Available projects

### ePassportViewer
- [Origin](https://github.com/andrew867/epassportviewer)
- [GitHub mirror](https://github.com/andrew867/epassportviewer)

It is supported by pypassport python library, which can be found in the same repository.

There is a [version of pypassport 2.0](https://github.com/landgenoot/pypassport-2.0) available which claims:
> "added support for Dutch ECDSA Active Authentication"

These projects have been actively investigated. It takes some time to get all the needed software installed since main project was last updated 4 years ago. But the viewer and pypassport library are working.
We get stuck at reading the passport information.

To experiment with changes in the pypassport library you need to reinstall it every time.
This is done inside a virtual environment.

#### Changes we made so far

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

#### Processing face image

The face image is located in DG2 (DG is short for Data Group), corrosponding with tag '75', more info about this can be found at ICAO Doc 9303. It is formatted in JPEG2000 (jp2), so in order to use it properly it should be converted to another format like jpg or png.

The pypassport module provides some code thats shows how to do this, but in order for this to work some libraries have to installed first.

First install (JasPer)[http://www.ece.uvic.ca/~frodo/jasper/], this used by GraphicsMagick and handles JPEG2000 files
It is available (here)[https://github.com/mdadams/jasper], but I had trouble building it from here.

```
# git clone https://github.com/xorgy/graphicsmagick // this is a large download, but couldn't get it working otherwise
# cd graphicsmagick/jp2
# export CFLAGS="-O2 -fPIC" // this is important later when installing GraphicsMagick
# ./configure
# make
# sudo make install
```

Then install GraphicsMagick, image processing software, from anywhere (here)[http://www.graphicsmagick.org/download.html], I used version 1.3.30.
```
# 'Download from web & enter folder'
# ./configure --with-modules --enable-shared=yes // is has to be shared in order for pgmagick to use it
# make
# sudo make install
# ldconfig // 'For security and performance reasons, Linux maintains a cache of the shared libraries installed in "approved" locations and this command will update it.'
```

GraphicsMagick should support JPEG2000 now, you can check this by running:
```
# gm version
```
It should list `JPEG-2000 ... yes` under `Feature Support`.

Finally install (pgmagick)[https://github.com/hhatto/pgmagick], which is a boost.python based wrapper for GraphicsMagick
```
# git clone https://github.com/hhatto/pgmagick
# python setup.py install
```
Do not install pgmagick through `pip`, this version includes its own version of GraphicsMagick which will not support JPEG2000.

### JMRTD
> "An Open Source Java Implementation of Machine Readable Travel Documents"

Used by ReadID app.
Has not been investigated yet.


## Relevant information

The standard around Machine Readable Travel Documents can be found at [ICAO Doc 9303](https://www.icao.int/publications/pages/publication.aspx?docnum=9303)
