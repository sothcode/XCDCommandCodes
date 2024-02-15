#!/usr/bin/python3

# This is designed to tell a particular egg to steer to a given (theta,phi) coordinate pair

from goto import goto
from changeAxisDogleg import changeAxis
import sys



# to load tty data from the db so we know which tty we want:
sys.path.append("kfDatabase")
import kfDatabase

mainDb="test_only_axis_parameters.kfdb"


def _reverseLookup(dict,val):
    #set up the reverse dictionary
    reverse_mapping={v: k for k, v in dict.items()}
    try:
        key=reverse_mapping[val]
    except KeyError as e:
        print(f"_reverseLookup failed.  KeyError: {e}")
        sys.exit()
    return key  

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    
def countBounces(theta):
    # count the number of bounces in the light pipe's x direction and y-direction,
    # also report back if the desired theta is very close to exiting at an edge.
    # if we are at an edge, we will need to do some special calculation/steering

    # rcc:  for now, assume we are not close to an edge, and assume zero bounces
    return False,0,0

def debounce(phi, bouncesX, bouncesY):
    #I might have gotten X and Y confused...
    if (bouncesX % 2 == 1): #if we bounce against X=0 once, we get reflected about the Y axis
        phi=180-phi
    if (bouncesY % 2 == 1): #if we bounce against Y=0 once, we get reflected about the X axis
        phi=-phi
        
    return phi
        
def getPhiMotorCoordinate(eggName,phi):
    #look up the position that points at phi0 (=pointing outward(or inward?  ask Charles) along the radial spoke)
    #TODO: phi0=kfDatabase.readVar(mainDb,eggName+"_PH/phi0")
    lb=kfDatabase.readVar(mainDb,eggName+"_PH/lowbound")
    hb=kfDatabase.readVar(mainDb,eggName+"_PH/highbound")
    phi0=0 #for now
    phiInTurns=phi/360.0
    phiCoord=phiInTurns+phi0
    #TODO: determine whether this rotates clockwise or counterclockwise, and fix it so it agrees with Charles' convention

    #check if this is in bounds for this egg.  if not, add/subtract 1.0
    if phiCoord>hb:
        phiCoord=phiCoord-1.0
    elif phiCoord<lb:
        phiCoord=phiCoord+1.0

    if (phiCoord<lb):
        print("desired target %s is out of range for %s matter what we do.  range=[%s,%s].  Failing."%(phi,eggName,lb,hb))
        sys.exit()
    return phiCoord


def aimAt(laserName="DEBUG",eggName=None, theta=None, phi=None):
    #assume we have phi and theta in degrees

    #TODO: sanity check the inputs

    tooCloseToEdge,bouncesX, bouncesY=countBounces(phi,theta)

    #TODO:
    # if tooCloseToEdge:
    #     doExtraCalculations to find the offset that gets us a safe trajectory?
    # or maybe we want the ability to steer /along/ the edge, for calibration purposes?

    debouncedPhi=debounce(phi, bouncesX,bouncesY)

    #TODO: see if this is in the lb-hb range of the phi motor, and add a bounce if it is not
    
    phiCoord=getPhiMotorCoordinate(eggName,debouncedPhi)
    #TODO:  this or similar?  thetaS,thetaL=getThetaMotorCoordinates(eggName,theta)

    retPh=goto(laserName+"_PH",phiCoord)
    #retThS=goto(laserName+"_TH_S",thetaS)
    #retThL=goto(laserName+"_TH_L",thetaL)
 



if __name__ == "__main__":
    #check args
    if len(sys.argv)==4:
        #assume (eggDbName,theta,phi).
        #TODO:  specify which laser (port,axis), and which egg?  Or should we mate those permanently in the db?
        #get its port from the db
        egg=sys.argv[1]
        theta=sys.argv[2]
        phi=sys.argv[3]
    else:
        print("NOT EXECUTED. Wrong number of arguments.  Correct usage is:")
        print("   ./steetTo.py egg_name theta phi")
        sys.exit()
    #if wrong arguments, exit with explanation

    steerTo("DEBUG",eggName,theta,phi)
