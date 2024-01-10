#!/usr/bin/python3
import re
from helper import *

warningblocks = 5000
testwarning = False
testerror = False
debug = False

printHEADER("Checking Participation Key")

# Goal participation key stats gathering 
goal = runCommand(['goal','account','partkeyinfo'])
goalcmd = re.search(r"Effective last round:\s+(\d+)",goal)
lastround = int(goalcmd.group(1))

goalcmd = re.search(r"Last vote round:\s+(\d+)",goal)
lastvote = int(goalcmd.group(1))

diff = lastround - lastvote

if (testwarning):
  diff = warningblocks - 1
if (testerror):
  diff = -10

if (debug):
  print ("lastround = " + str(lastround) + ", lastvote = " + str(lastvote) + ", diff = " + str(diff) + ", warningblocks = " + str(warningblocks))

if (diff > warningblocks):
  printOK(str(diff) + " blocks until your key stops working")
elif (diff > 0):
  printWARNING(str(diff) + " blocks until your key stops working")
else:
  printERROR("Your key expired " + str(diff) + " blocks ago")