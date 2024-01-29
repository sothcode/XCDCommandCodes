# XCDCommandCodes
Commands to control the XCD Evaluation kit using USB


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
