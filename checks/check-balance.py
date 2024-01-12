#!/usr/bin/python3
import re
import os
from helper import *

lowVOI = 100 
suggestedVOI = 550

printHEADER("Checking Balance")

goal = runCommand(["goal", "account", "dump", "-a", os.environ["addr"]])
goalcmd = re.search(r"\"algo\"\:\s+(\d+)",goal)
balance = int(goalcmd.group(1))

if (balance >= (suggestedVOI * 1000000)):
  printOK(str(round(balance / 1000000,2)) + " VOI is enough")
elif (balance <= (lowVOI * 1000000)): 
  printERROR(str(round(balance / 1000000,2)) + " VOI is a _lot_ less than optimal - add via the Discord faucet until you have more VOI until you have " + str(suggestedVOI))
else:
  printWARNING(str(round(balance / 1000000,2)) + " VOI is less than optimal (" + str(suggestedVOI) +" or more)")
