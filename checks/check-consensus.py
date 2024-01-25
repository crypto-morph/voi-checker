#!/usr/bin/python3
import re
import os
from helper import *

printHEADER("Checking Consensus")
addr = os.environ["addr"]
avgPctOnTime = 0

goal = runCommand(["curl", "-s", "https://analytics.testnet.voi.nodly.io/v0/consensus/accounts/all"])
goalcmd = re.search(r"\s+\[\"" + addr + "\"\,\s+\"(\d+)\"\,\s+\"(\d+)\"\,\s+\"(\d+)\"\,\s+\"(\d+)\"\,\s+(\d+)\,\s+\"(\d+)\"\,\s+\"([^,]+)\"\,\s+([^,]+),\s+([^,]+),\s+(.+)\]\,",goal)
if goalcmd is not None: 
  avgPctOnTime = float(goalcmd.group(10))
else:
  printERROR('Checker failed to get consensus output from analytics.testnet.voi.nodly.io')
if (avgPctOnTime > 80):
  printOK("good average percentage on time - " + str(avgPctOnTime) + "%")
else: 
  printWARNING("low average percentage on time - " + str(avgPctOnTime) + "%")
