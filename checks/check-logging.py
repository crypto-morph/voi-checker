#!/usr/bin/python3
import json
from helper import *

printHEADER("Checking Logging")

f = open('/var/lib/algorand/logging.config')
data = json.load(f)
f.close()

if data['Enable']:
  printOK("Logging enabled")
else:
  printERROR("Logging set to '" + str(data['Enable']) + "'")
if (data['Name'] == ""):
  printERROR("Logging 'Name' not set - see /var/lib/algorand/logging.config")
else:
  printOK ("Logging Name set to '" + data['Name'] + "'")
printINFO("GUID starts '" + data['GUID'][:13] + "'")