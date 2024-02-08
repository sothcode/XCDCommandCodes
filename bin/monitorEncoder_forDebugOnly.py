#!/bin/python3

from quickAssign import sendcommand, writeXCD2
from quickReport import reportXCD2specifyAxis
from variableDictionaryXCD2 import varInterfaceAddresses as ADDR

print("Monitoring both encoders on channel set by XCD_current_port:")

while True:
    s0,enc0=reportXCD2specifyAxis(0,[ADDR['ENR']])
    s1,enc1=reportXCD2specifyAxis(0,[ADDR['ENR']])
    print("Enc0:%1.6f%s\tEnc1:%1.6f%s"%(enc0,"(error)"*s0,enc1,"(error)"*s1))
    
