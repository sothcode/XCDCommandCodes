#! /usr/bin/python3

from talkNano import main

from moveNano import moveNano
from assignNano import assignNano
from homeNano import homeNano
from killNano import killNano
from reportNano import reportNano
from pulseNano import pulseNano
from configRevNano import configRevNano
from configNano import configNano

import sys

commDict = {
"move"      : moveNano,
"assign"    : assignNano,
"home"      : homeNano,
"kill"      : killNano,
"report"    : reportNano,
"pulse"     : pulseNano,
"configRev" : configRevNano,
"config"    : configNano,
}
