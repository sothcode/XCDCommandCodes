#!/usr/bin/python3
import time
import serial
#import sys


def _readline(ser):
    eol = b'\r'
    leneol = len(eol)
    line = bytearray()
    while True:
        c = ser.read(1)
        if c:
            line += c
            if line[-leneol:] == eol:
                break
        else:
            break
    return bytes(line)


def readMKS(inputLine = 'ID'):
    # configure the serial connections (the parameters differs on the device you are connecting to)
    ser = serial
    #print ("Open the port")
    try:
        ser = serial.Serial(
            port='/dev/ttyUSB3',
            baudrate=115200,
            parity=serial.PARITY_ODD,
            bytesize=serial.EIGHTBITS
        )
        #ser.open()
        if (ser.isOpen()):
            phrase = b'\xE4\x
            inpt = str.encode('{}\r'.format(inputLine))
            #print ("Write")
            ser.write(inpt)
            #print ("Read")
            response = '{}'.format(_readline(ser))
            #print (response)
            #ser.close()
            return response
        return "9999999"

    except serial.serialutil.SerialException:
        return "eeeeeee"
        

#
# Move          1  Pos(Real-4)
# Assign16      2  var(ID-2)      Value(Int16-4)
# Assign        3  var(ID-2)      Value(Real-4)
# Home          4  method(Int-1) {origin(Real-4) velocity1(Real-4) velocity2(Real-4)}
# VelocityLoop  6  velocity(Real)
# OpenLoop      7  command(Real4)
# Save         13  addr(Int-1)    0x5A(Int-1)
# SetAddr      16  addr(Int-1)    0x5A(Int-1)    newaddr(Int-1)
# Enable       17
# Disable      18
# ReadVersion  19
# Monitor      20  chan(Int-1)    var(ID-2)      scale(Real-4)
# MonitorAddr  21  chan(Int-1)    addr(Int16-2)  scale(Real-4)
# Kill         23
# ReportInt16  25  var1(Int16-2)  var2(Int16-2)  ...             varN(Int16-2)     // for N up to 10
# Report       26  var1(ID-2)     var2(ID-2)     ...             varN(ID-2)        // for N up to 10
# PosPulseIncr 33  start(Real-4)  incr(Real-4)   count(Int32)
# GetRevision  55
# config       80  PWMvalue(Real) PWMwidth(Real) Thresh(Real)
# getvar      960  ID(Real)      {bit(Real)}
#
# ID          Name
# 900         Status
# 901         ProgStatus
# 902         SafetyDisable
# 903         SafetyInverse
# 904         SafetyState
# 905         IO-Direction
# 906         DZMIN
# 907         PWM-Limit
# 908         AIN-Protection
# 921-924     SPI-Input-Integer
# 925-926     SPI-Input-Real
# 950         XMS-checksum
# 951         XMS-length
# 960         Last-error
# 990         UART-address
# 991         IIC-address
#
#

