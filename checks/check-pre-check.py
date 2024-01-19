#!/usr/bin/python3
import subprocess
import pkg_resources
from helper import *

printHEADER("Pre-Flight-Checks")

status, result = subprocess.getstatusoutput("goal")
if (status != 0):
  printERROR('goal not found - check algorand package is installed')
else:
  printINFO('goal command is present')

required = {'psutil', 'speedtest-cli'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
  printERROR(missing + ' is missing - run `pip install psutils` - see README for details')
else:
  printINFO(" ".join(required) + ' are all installed')