#!/usr/bin/python3
import re
from helper import *

printHEADER("Check Versions")

goal = runCommand(['goal','version','-v'])
x = re.search(r"Build:\s+(\S+)",goal)
printINFO("goal version - " + x.group(1))