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

ePassportViewer,
- [Origin](https://github.com/andrew867/epassportviewer)
- [GitHub mirror](https://github.com/andrew867/epassportviewer)

supported by pypassport python library, which can be found in the same repository.

There is a version of pypassport 2.0 available which claims:
> "added support for Dutch ECDSA Active Authentication"

- [pypassport 2.0 by landgenoot](https://github.com/landgenoot/pypassport-2.0)

These projects have been actively investigated. It takes some time to get all the needed software installed since main project was last updated 4 years ago. But the viewer and pypassport library are working.
We get stuck at reading the passport information.
