# Decode Passport Scanner

This Passport Scanner is part of the Decode Amsterdam project. For more extended information check out the [Decode Amsterdam]() repository.

In this repository you will everything you need to create your own Passport Scanner. It could be used stand alone to read data of the NFC chip inside a passport, but it's full potential is to read the data and then make it available from transfer to the Decode Amsterdam PWA.

**Important note:**
This project was created as a proof of concept prototype. There for it was never meant to be used on a large scale but for demonstration purposes only.

In this repository you will find the following:

* Code for communication with different hardware elements
* Code for communication with the [Decode Session Manager]()
* Documentation for building a physical box to combine all hardware elements 

The code and hardware has only been tested using Ubuntu 18.04.


## Hardware

There are different hardware elements needed to get the party started.

### NFC Reader

Before we start it is good to mention there is a specific library being used to handle all the complicated interaction between a NFC scanner and the NFC chip in a passport. This library, PyPassport, needed to be modified slightly in order to work with the NFC readers we had available. This modified version can be found as a submodule of this project and [here](). The library it self is using the standard of Machine Readable Travel Documents (MRTD) as defined in [ICAO Doc 9303](https://www.icao.int/publications/pages/publication.aspx?docnum=9303). 

The NFC reader we ended up using is the [ACS ACR1252U-M1](https://www.acs.com.hk/en/products/342/acr1252u-usb-nfc-reader-iii-nfc-forum-certified-reader/), supported by the [CCID driver](https://ccid.apdu.fr/).

#### Testing the NFC Reader

List all USB devices: `$ lsusb`

Using the [PCSC-lite](https://pcsclite.apdu.fr/) daemon `pcscd` you can check if the driver is compatible with a NFC scanner:
`$ sudo pcscd -f -d`

Start PCSC in the background:
`$ service pcscd start`

Using [pcsc-tools](http://ludovic.rousseau.free.fr/softwares/pcsc-tools/) chips on the scanner can be read, PCSC needs te be started for this:
`$ pcsc_scan`


### Camera

The camera is used to read the MRZ (Machine Readable Zone) on a passport which on its turn it used to decrypt the data on the passport's NFC chip.

Any modern webcam will do, as long as it has a decent resolution to perform OCR. We ended up using the [Razer Kiyo](https://www.razer.com/gaming-broadcaster/razer-kiyo). We modified it by removing the stand so only the camera was left, this way it fit nicely in the box.


## Setup




## Run

There must be a file present named `mrz.json` containing the MRZ of the document thats on the scanner.
Also a folder named `output` must be present.

```
$ python reader.py
```


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


## Relevant information

The standard around Machine Readable Travel Documents can be found at [ICAO Doc 9303](https://www.icao.int/publications/pages/publication.aspx?docnum=9303)
