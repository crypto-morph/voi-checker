#!/usr/bin/python3
import re
import os
from helper import *
from pathlib import Path

printTITLE("VOI Participation Node Checker")
printHEADER("Checking Node")
addr = os.environ["addr"]
printINFO("VOI address is " + addr)

# First, check we are running VOI Swarm
swarmEnabled = swarmEnabled()

# Second, check systemctl exists - if it doesn't we're probably not installed using D13s guide
if (os.path.isfile('/usr/bin/systemctl')):
  printOK('systemctl detected (likely a D13 setup)')
else:
  printWARNING('systemcl NOT detected - this checker only works with D13 setup (see Readme)')

# Is the node running?
if (os.path.isfile('/etc/supervisor/conf.d/supervisord.conf')):
  printWARNING('supervisord available - could be in a container - so no checking systemctl')
else:
  checkactive = runCommand(["systemctl", "is-active", "voi"]).strip()
  if (checkactive == "active"):
    printOK("VOI Systemctl Node is started")
  elif (swarmEnabled):
    printOK("VOI Systemctl Node is not started - but Swarm VOI detected")
  else:
    printERROR("VOI Systemctl Node isn't started and Swarm VOI NOT detected")

# Is the node synced?
goal = runCommand(['goal','node','status'])
goalcmd = re.search(r"Sync Time:\s+(\d+\.\d+)s",goal)
if (float(goalcmd.group(1)) == 0.0):
  printOK("Node is in sync")
else:
  printERROR("Node is out of sync - sync has been running for " + str(goalcmd.group(1)))

# Is the node online?
goal = runCommand(['goal','account','dump', '-a', addr ])
goalcmd = re.search(r"\"onl\":\s+(\d+),",goal)
if (int(goalcmd.group(1)) == 1):
  printOK("Node is in online")
else:
  printERROR("Node is offline - status " + str(goalcmd.group(1)))
