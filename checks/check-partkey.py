#!/usr/bin/python3
import re
from helper import *

warningblocks = 5000
testwarning = False
testerror = False
debug = False

printHEADER("Checking Participation Key")

# Goal participation key stats gathering 
mylastround = 0

goal = runCommand(['goal','node','lastround'])
thisround = int(goal)
if (thisround < 1):
  printERROR("Node not reporting last round")

goal = runCommand(['goal','account','partkeyinfo'])
goalcmd = re.search(r"Effective last round:\s+(\d+)",goal)
mylastround = 0
if goalcmd is not None:
   mylastround = int(goalcmd.group(1))
else:
   printERROR("Node not reporting Effective Last round")

diff = mylastround - thisround

if (testwarning):
  diff = warningblocks - 1
if (testerror):
  diff = -10

if (diff > warningblocks):
  printOK(str(diff) + " blocks until your key stops working")
elif (diff > 0):
  printWARNING(str(diff) + " blocks until your key stops working")
else:
  printERROR("Your key expired " + str(diff) + " blocks ago")
