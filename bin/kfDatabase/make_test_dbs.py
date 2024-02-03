#!/bin/python3
import sys
import os
sys.path.append("kfDatabase")
import kfDatabase as kf


testports="test_only_xcd2_ports.kfdb"
if not(os.path.exists(testports)): #if it doesn't exist, touch it so it does.
    with open(testports, 'w'):
        pass
kf.writeVar(testports,"DEBUG_DL0_A0",["dev_test_only",0],"new")
kf.writeVar(testports,"DEBUG_DL0_A1","dev_test_only","new")
kf.writeVar(testports,"DEBUG_DL1_A0","dev_test_only1","new")
kf.writeVar(testports,"DEBUG_DL1_A1","dev_test_only1","new")
kf.writeVar(testports,"DEBUG_TH_S","dev_test_only2","new")
kf.writeVar(testports,"DEBUG_TH_L","dev_test_only2","new")
kf.writeVar(testports,"DEBUG_PH","dev_test_only3","new")
kf.writeVar(testports,"DEBUG_AT","dev_test_only3","new")
kf.listVar(testports)

testparameters="test_only_axis_parameters.kfdb"
if not(os.path.exists(testparameters)): #if it doesn't exist, touch it so it does.
    with open(testparameters, 'w'):
        pass
kf.writeVar(testparameters,"DEBUG_DL0_A0/align",0,"new")
kf.writeVar(testparameters,"DEBUG_DL0_A0/home",0.2,"new")
kf.writeVar(testparameters,"DEBUG_DL0_A1/align","0","new")
kf.writeVar(testparameters,"DEBUG_DL0_A1/home","0.3","new")

kf.writeVar(testparameters,"DEBUG_DL1_A0/align","0","new")
kf.writeVar(testparameters,"DEBUG_DL1_A0/home","0.2","new")
kf.writeVar(testparameters,"DEBUG_DL1_A1/align","0","new")
kf.writeVar(testparameters,"DEBUG_DL1_A1/home","0.3","new")

kf.writeVar(testparameters,"DEBUG_TH_S/home","0","new")
kf.writeVar(testparameters,"DEBUG_TH_S/upstream","0.5","new")
kf.writeVar(testparameters,"DEBUG_TH_S/downstream","-0.5","new")
kf.writeVar(testparameters,"DEBUG_TH_S/diode0","0.03","new")
kf.writeVar(testparameters,"DEBUG_TH_S/diode1","0.035","new")
kf.writeVar(testparameters,"DEBUG_TH_S/diode2","0.033","new")

kf.writeVar(testparameters,"DEBUG_TH_L/home","0","new")
kf.writeVar(testparameters,"DEBUG_TH_L/park","0.5","new")
kf.writeVar(testparameters,"DEBUG_TH_L/short_align","-0.11","new")
kf.writeVar(testparameters,"DEBUG_TH_L/lowbound","-0.2","new")
kf.writeVar(testparameters,"DEBUG_TH_L/highbound","0.7","new")
kf.writeVar(testparameters,"DEBUG_TH_L/diode0","0.13","new")
kf.writeVar(testparameters,"DEBUG_TH_L/diode1","0.135","new")
kf.writeVar(testparameters,"DEBUG_TH_L/diode2","0.133","new")

kf.writeVar(testparameters,"DEBUG_PH/home","0","new")
kf.writeVar(testparameters,"DEBUG_PH/lowedge","0.1","new")
kf.writeVar(testparameters,"DEBUG_PH/highedge","0.7","new")
kf.writeVar(testparameters,"DEBUG_PH/diode0","0.13","new")
kf.writeVar(testparameters,"DEBUG_PH/diode1","0.135","new")
kf.writeVar(testparameters,"DEBUG_PH/diode2","0.133","new")

kf.writeVar(testparameters,"DEBUG_AT/home","0","new")
kf.writeVar(testparameters,"DEBUG_AT/lowedge","0.1","new")
kf.writeVar(testparameters,"DEBUG_AT/highedge","0.7","new")
