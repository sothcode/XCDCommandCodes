Commands to control the Direct Laser controllers and the XCD Evaluation kit using USB

Direct Laser Alignment commands:

(all in XCDCommandCodes/bin)

./executeXMS.sh -- starts the XMS, which is automatic when the device is powered

./stopXMS.sh -- stops the XMS, eg if in a broken loop.

./clearDogleg.py -- resets error states in the controller status.  8=nack, 9=busy, 1=fail, 98=rebooted

./homeDogleg.py -- moves the current axis to home and keeps track of rotations.  stops if |rotations|>3

./gotoDogleg.py 3.1 -- moves the current axis to absolute position 3.1, with occasional backs to unbind.   stops if |rotations|>3

./gotoDogleg.py L0_DL0_A0 1.7 -- moves axis A0 on DogLeg 0 to absolute position 1.7.  If that axis is not what is currently being controlled, it saves the current axis data to a file, then loads the correct axis data from the named file before moving.

./relativeDogleg.py -0.5 -- moves the current axis -0.5 from its current position , with occasional backs to unbind.  stops if |rotations|>3



if needed:
./quickAssign.py XAXIS 1 -- switches the current axis to axis 1 (other data will not be updated).  Use '0' to switch to zero.
./changeAxisDogleg.py L0_DL0_A0 -- switches the axis to axis 0 for dogleg 0 on laser 0, and loads the last known variables for that axis from file to the controller, if the file exists.  Writes out the current file for the current axis as well.

Files:

XCD Commands:
  talkNano.py: 
  
  readNano.py

  {assign, config, configRev, home, kill, move, pulse, report}Nano.py: individual motor command scripts
  
  cmdNano.py: high level command
  
  variableDictionary.py: dictionary of XCD variables, used in some commands
  
  commandDictionary.py: dictionary of XCD commands, used in cmdNano.py
  
XCD2 Commands:

Other:
  SetupXCD.sh: sets serial port baud rate in bash
  Home{Right, Left}.sh: sends XCD home command in bash
  
Ignore:
  playNano:
