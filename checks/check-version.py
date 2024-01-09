#!/usr/bin/python3
import subprocess
import re

def printOK(mystring):
  print ('\033[92m OK - ' + mystring + '\033[0m')
def printERROR(mystring):
  print ('\033[91m ERROR - ' + mystring + '\033[0m')
def printINFO(mystring):
  print ('\033[94m INFO - ' + mystring + '\033[0m')

goal = subprocess.check_output(['goal','version','-v']).decode('utf-8')
x = re.search(r"Build:\s+(\S+)",goal)
printINFO("goal version - " + x.group())
