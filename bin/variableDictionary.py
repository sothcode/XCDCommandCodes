#! /usr/bin/python3

import sys

varDict = {
#Required Motion Parameters
"VEL"  : 1,    # Velocity [mm/sec]
"ACC"  : 2,    # Acceleration [mm/sec^2]
"KDEC" : 4,    # Kill Deceleration

# Instant Reference Motion Variables
"TPOS" : 5,    # Target Position
"RPOS" : 6,    # Reference Position
"RVEL" : 7,    # Reference Velocity
"RACC" : 8,    # Reference Acceleration

# Instant Feedback Motion Variables
"FPOS" : 9,    # Feedback Position
"FVEL" : 10,   # Feedback Velocity
"PE"   : 12,   # Position Error
"POSI" : 52,   # Position latched on index pulse

# Time Variables
"TIME" : 38,   # Elapsed time in milliseconds
"PPW"  : 54,   # Position compare pulse width in milliseconds

# Servo Loop and Drive Configuration
"KP"   : 13,   # Position Loop Gain
"KV"   : 14,   # Velocity Loop Gain
"LI"   : 16,   # Velocity Loop Integrator Limit
"BQA1" : 17,   # First Bi-Quad filter parameters
"BQA2" : 18,
"BQB0" : 19,
"BQB1" : 20,
"BQB2" : 21,
"BQ2A1": 67,   # Second B-Quad filter parameters
"BQ2A2": 68,
"BQ2B0": 69,
"BQ2B1": 70,
"BQ2B2": 71,
"ENR"  : 22,   # Encoder Resolution [milliseconds per 1 encoder count]
"MFREQ": 23,   # Motor Frequency (PWM frequency)
"SPRD" : 24,   # Servo Loop Sampling period [milliseconds]
"DZMIN": 40,   # Dead zone min
"DZMAX": 41,   # Dead zone max
"ZFF"  : 42,   # Zero feed forward
"FRP"  : 43,   # Friction in positive direction
"FRN"  : 44,   # Friction in negative direction
"DOUT" : 45,   # Instant drive output (% of maximal output)

#Safety
"DOL"  : 39,   # Drive output limit (% of maximal output)
"DOFFS": 53,   # Drive output offset (% of maximal output)
"SLP"  : 47,   # Software limit positive
"SLN"  : 48,   # Software limit negative
"PEL"  : 49,   # Position error limit
"MTL"  : 51,   # Motion Time limit

# Analog Inputs/Outputs
"AIN0" : 30,   # Analog Inputs (%)
"AIN1" : 31,
"AIN2" : 32,
"AIN3" : 33,
"AIN4" : 55,
"AIN5" : 56,
"AIN6" : 57,
"AIN7" : 58,
"AIN8" : 59,
"AIN9" : 60,
"AIN10": 61,
"AIN11": 62,
"AIN12": 63,
"AIN13": 64,
"AIN14": 65,
"AIN15": 66,
"AOUT0": 34,   #Analog Output (%)
"AOUT1": 35,
"AOUT2": 36,
"AOUT3": 37,

# Pseudovariables
"Status"              : 900,
"Program Status"      : 901,
"Safety Disable"      : 902,
"Safety Inverse"      : 903,
"Safety State"        : 904,
"IO Direction"        : 905,
"DZMIN Blackout"      : 906,
"PWM Limit"           : 907,
"AIN Protection"      : 908,
"SPI Input Integer 1" : 921,
"SPI Input Integer 2" : 922,
"SPI Input Integer 3" : 923,
"SPI Input Integer 4" : 924,
"SPI Input Real 1"    : 925,
"SPI Input Real 2"    : 926,
"XMS Checksum"        : 950,
"XMS Length"          : 951,
"Last Error"          : 960,
"UART Address"        : 990,
"IIC Address"         : 991,


}


