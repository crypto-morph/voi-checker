#!/usr/bin/python3
import re
from helper import *

def versiontuple(v):
    return tuple(map(int, (v.split("."))))

printHEADER("Check Versions")

goal = runCommand(['goal','version','-v'])
x = re.search(r"Build:\s+(\d+\.\d+\.\d+)",goal)
version = x.group(1)

printINFO("goal version - " + version)

if (versiontuple(version) < versiontuple("3.21.0")):
  printERROR("This version " + version + " is less than 3.21.0 - some scripts may not run")