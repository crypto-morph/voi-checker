#!/usr/bin/python3
import json

def printOK(mystring):
  print ('\033[92m OK - ' + mystring + '\033[0m')
def printERROR(mystring):
  print ('\033[91m ERROR - ' + mystring + '\033[0m')
def printINFO(mystring):
  print ('\033[94m INFO - ' + mystring + '\033[0m')

print ("Checking Logging...")

f = open('/var/lib/algorand/logging.config')
data = json.load(f)

if data['Enable']:
  printOK("Logging enabled")
else:
  printERROR("Logging set to '" + str(data['Enable']) + "'")
if (data['Name'] == ""):
  printERROR("Logging 'Name' not set - see /var/lib/algorand/logging.config")
else:
  printOK ("Logging Name set to '" + data['Name'] + "'")
f.close()
printINFO("GUID starts '" + data['GUID'][:13] + "'")


