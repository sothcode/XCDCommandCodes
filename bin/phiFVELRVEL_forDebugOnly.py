#! /usr/bin/python3

import sys
import time
from quickAssign import sendcommand
from quickReport import readback, reportXCD2
from variableDictionaryXCD2 import varDict
from variableDictionaryXCD2 import varPhiCommands as COMM

if len(sys.argv) == 2:
    destination = sys.argv[1]
else:
    sys.exit()

print('Monitoring reference and feedback velocites for phi goto.')

commandSent=sendcommand(COMM['GOTO'],destination) # this sleeps until it sees the status change from new_command
if not commandSent:
    sys.exit()

while True:
    sp,FPOS=reportXCD2(['FPOS'])
    sv,VELS=reportXCD2(['FVEL', 'RVEL'])
    print("FPOS:%1.6f%s\tFVEL:%1.6f%s\tRVEL:%1.6f%s"%(FPOS[0],"(error)"*(not sp),VELS[0],"(error)"*(not sv),VELS[1],"(error)"*(not sv)))
