# Passport reading

## Testing scanner

The scanner we're using the [ACS ACR1252U-M1](https://www.acs.com.hk/en/products/342/acr1252u-usb-nfc-reader-iii-nfc-forum-certified-reader/) scanner, supported by the [CCID driver](https://ccid.apdu.fr/). All done on a Ubuntu machine.

List all USB devices:
`lsusb`

Using the [PCSC-lite](https://pcsclite.apdu.fr/) daemon `pcscd` you can check if the driver is compatible with a NFC scanner:
`sudo pcscd -f -d`

Start PCSC in the background:
`service pcscd start`

Using [pcsc-tools](http://ludovic.rousseau.free.fr/softwares/pcsc-tools/) chips on the scanner can be read, PCSC needs te be started for this:
`pcsc_scan`

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

The face image is located in DG2 (DG is short for Data Group), corrosponding with tag '75', more info about this can be found at ICAO Doc 9303. It is formatted in jp2 (JPEG2000), so in order to use it properly it should be converted to another format like jpg or png.
The pypassport module provides some code to do this, but in order for this to work some libraries have to installed first.
Source: https://serverfault.com/questions/766324/imagemagick-and-openjpeg2
```
sudo apt-get install cmake
wget https://github.com/uclouvain/openjpeg/archive/version.2.1.tar.gz
tar xzf version.2.1.tar.gz
cd openjpeg-version.2.1/
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr
make
sudo make install

sudo apt-get install libperl-dev
wget http://www.imagemagick.org/download/ImageMagick.tar.gz
tar xzf ImageMagick.tar.gz
cd ImageMagick-6.9.3-8
./configure --prefix=/usr --with-modules --with-perl=/usr/bin/perl --with-jp2 --enable-shared --disable-static --without-magick-plus-pus
make
sudo make install

convert -list configure | grep DELEGATES
```
Check if openjp2 is in the list printed by the last command.

### JMRTD
> "An Open Source Java Implementation of Machine Readable Travel Documents"

Used by ReadID app.
Has not been investigated yet.


## Relevant information

The standard around Machine Readable Travel Documents can be found at [ICAO Doc 9303](https://www.icao.int/publications/pages/publication.aspx?docnum=9303)
