#!/usr/bin/python3
import re
import os
from helper import *

printHEADER("Checking Balance")

goal = runCommand(["goal", "account", "dump", "-a", os.environ["addr"]])
goalcmd = re.search(r"\"algo\"\:\s+(\d+)",goal)
balance = int(goalcmd.group(1))

if (balance >= 550000000):
  printOK(str(balance / 1000000) + " voi is enough")
else: 
  printERROR(str(balance / 1000000) + " is NOT enough")
