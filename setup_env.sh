#!/bin/bash
sudo apt update
# core
sudo apt install git python python-pip virtualenv
# nfc
sudo apt install pcscd pcsc-tools swig libpcsclite-dev
# ocr
sudo apt install python-tk tesseract-ocr libtesseract-dev
service pcscd start
git clone https://github.com/sguldemond/passport_reading.git mrtd_reader
cd mrtd_reader
git clone https://github.com/sguldemond/pypassport pypassport
virtualenv -p /usr/bin/python2.7 python2
source python2/bin/activate
pip install ./pypassport
pip install git+git://github.com/ojii/pymaging.git#egg=pymaging
pip install git+git://github.com/ojii/pymaging-png.git#egg=pymaging-png
pip install -r clean_requirements.txt
