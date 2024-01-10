#!/usr/bin/python3
import re
import os
from helper import *

printHEADER("Checking Consensus")
addr = os.environ["addr"]

goal = runCommand(["curl", "-s", "https://analytics.testnet.voi.nodly.io/v0/consensus/accounts/all"])
goalcmd = re.search(r"\s+\[\"" + addr + "\"\,\s+\"(\d+)\"\,\s+\"(\d+)\"\,\s+\"(\d+)\"\,\s+\"(\d+)\"\,\s+(\d+)\,\s+\"(\d+)\"\,\s+\"([^,]+)\"\,\s+([^,]+),\s+([^,]+),\s+(.+)\]\,",goal)
avgPctOnTime = float(goalcmd.group(10))
if (avgPctOnTime > 80):
  printOK("good average percentage on time - " + str(avgPctOnTime) + "%")
else: 
  printERROR("low average percentage on time - " + str(avgPctOnTime) + "%")