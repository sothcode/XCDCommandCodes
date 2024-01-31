# sPHENIX Line Laser steering and controls software

Software package to actuate the primary and secondary steering of the line laser system for the sPHENIX TPC calibration

## TL;DR

### Commands

* `./executeXMS.sh` -- starts the XMS, which is automatic when the device is powered

* `./stopXMS.sh` -- stops the XMS, eg if in a broken loop.

* `./killXCD2.sh` -- stops the XMS, kills movement on both axes, and disables

* `./clearDogleg.py -- resets error states in the controller status.  8=nack, 9=busy, 1=fail, 98=rebooted

* `./homeDogleg.py -- moves the current axis to home and keeps track of rotations.  stops if |rotations|>3

* `./gotoDogleg.py 3.1 -- moves the current axis to absolute position 3.1, with occasional backs to unbind.   stops if |rotations|>3

* `./gotoDogleg.py L0_DL0_A0 1.7 -- moves axis A0 on DogLeg 0 to absolute position 1.7.  If that axis is not what is currently being controlled, it saves the current axis data to a file, then loads the correct axis data from the named file before moving.

* `./relativeDogleg.py -0.5 -- moves the current axis -0.5 from its current position , with occasional backs to unbind.  stops if |rotations|>3


if needed:
./quickAssign.py XAXIS 1 -- switches the current axis to axis 1 (other data will not be updated).  Use '0' to switch to zero.
./changeAxisDogleg.py L0_DL0_A0 -- switches the axis to axis 0 for dogleg 0 on laser 0, and loads the last known variables for that axis from file to the controller, if the file exists.  Writes out the current file for the current axis as well.


### "Fixed" Variables

## Description

The sPHENIX line laser system is used to generate particle tracks of know position and orientation, thus allowing identification of distortions 

An in-depth paragraph about your project and overview of use.

The primary and secondary steering of the sPHENIX TPC line laser system is actuated by Nanomotion Edge and Edge-4X motors.  These motors are controlled by the XCD2 controller which receives signals via serial communication from a Raspberry Pi 

## Getting Started

### Dependencies

Program requires python3 
* Describe any prerequisites, libraries, OS version, etc., needed before installing program.
* ex. Windows 10

### Installing

* How/where to download your program
* Any modifications needed to be made to files/folders

### Executing program


* How to run the program
* Step-by-step bullets
```
code blocks for commands
```

## Help

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Authors

Seth Howell
seth.howell@stonybrook.edu

Kristina Finnelli
kristina.finnelli@stonybrook.edu

## Version History

* 0.2
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release

## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.
* [awesome-readme](https://github.com/matiassingers/awesome-readme)
* [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
* [dbader](https://github.com/dbader/readme-template)
* [zenorocha](https://gist.github.com/zenorocha/4526327)
* [fvcproductions](https://gist.github.com/fvcproductions/1bfc2d4aecb01a834b46)
