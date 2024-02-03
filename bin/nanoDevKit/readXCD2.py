#!/usr/bin/python3
import time
import serial
#import sys


def _readline(ser):
    # read and interpret the reply's "header" and name it in bytes (5 bytes)
    e4 = ser.read(1) # Prefix - UART sync byte 1 (constant x\E4)
    a5 = ser.read(1) # Prefix - UART sync byte 2 (constant x\A5)
    a4 = ser.read(1) # Prefix - Destination Address (\x00 for XCD2 UART protocol)
    d5 = ser.read(1) # Prefix - Start index
    NN = ser.read(1) # Prefix - Packet length in bytes (includes start index, not sync bytes or address)
    NN = int.from_bytes(NN, "big")

    # read the requested number of bytes as stipulated in the header to read commands and arguments
    line = bytearray([NN])
    for i in range(0,NN-2):
        c = ser.read(1)
        if c:
            line += c
        else:
            break
        resp = e4 + a5 + a4 + d5 + bytes(line)
    return resp


def readXCD2(inputList = [228, 165, 0, 213, 4, 50]): #default list is for home command
    for i in range(0, len(inputList)):
        inputList[i] = int(inputList[i])
    ser = serial
    try:
        ser = serial.Serial(
            port='/dev/ttyUSB0', # Set serial port
            baudrate=115200,     # Set baud rate
            parity=serial.PARITY_NONE,
            bytesize=serial.EIGHTBITS
        )
        if (ser.isOpen()):
            phrase = bytes(inputList)
            ser.write(phrase)
            response = '{}'.format(_readline(ser))
            print(response)
            ser.close()
            return response
        return "9999999"

    except serial.serialutil.SerialException:
        return "Serial Exception- check to see that usb is properly connected, or motor is powered."

# XCD2 Commands, arguments
#
# Group 0 (Communication)
#
#
# Group 1 (System)
#
# Group 2 (Boot)
#
# Group 5 (Servo)
#
# Group 6 (Variable)
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

