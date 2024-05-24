
########################
#  NOVAPI SERIAL TEST  #
########################
# Thai Nichi Institute of Technology
#
# Since the python file is uploaded directly to the EEPROM, when you're using a mBlock 5 software.
# The code blocks you've edited is compiled back to python, then that file is uploaded to NovaPi.
# Which means that Novapi itself is running its own runtime to handle the python files. ideally Linux minimal install.
# And the NovaPi's EEPROM can be flashed with other files, not just a .py file.
# This means that the python file is not running on the host machine, but on the Novapi itself.
#
# Runtime file. NovaPi:/main.py
# Communicable: USB Linux:/dev/ttyUSB*, USB Windows: COM*, To use any UART devices (or CH341SER) on Linux: sudo chmod a+rw /dev/ttyUSB*
# Linux: screen /dev/ttyUSB* 115200, putty /dev/ttyUSB*
# mbuild pads: /dev/ttyS*
#
# What we're trying to do
# Computer[usb-ttl adapter] -> UART -> NovaPi's empty UART pad (probably mBuild compatible)

import novapi

try:
    import serial
    ser = serial.Serial("/dev/ttyS0", baudrate=115200, parity= serial.PARITY_NONE, stopbits= serial.STOPBIIS_ONE, bytesize= serial.EIGHTBITS, timeout= 1)

except ImportError:
    print("No package serial found!")

# The remaining code will be uploaded later.