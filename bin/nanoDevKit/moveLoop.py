#! /usr/bin/python3

import time

from commNano import main
from moveNano import moveNano
from statusNano import statusNano

import sys

def waitTillDone():
	while statusNano() == False:
		time.sleep(1)
	return

def moveLoop ( argv ):
	# ask whether or not movement is done
	# if movement is done, move the other way
	count = 0
	if argv:
		while count < int(argv[0]):
			moveNano(3)
			waitTillDone()
			moveNano(-3)
			waitTillDone()
			count += 1
			print("Finished move", count, "\n")
	# waitTillDone loops and checks status, holds if busy
	else:
		print(" \ Error")

if __name__ == "__main__":
	moveLoop(sys.argv[1:])
