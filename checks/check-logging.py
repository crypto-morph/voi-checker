#!/usr/bin/python3
import json
from helper import *

printHEADER("Checking Logging")

data = {}

if (swarmEnabled()):
  location = '/var/lib/voi/algod/data/logging.config'
else:
  location = '/var/lib/algorand/logging.config'
try:
  f = open(location)
  data = json.load(f)
  f.close()
except FileNotFoundError as e:
    printERROR(location + " isn't readable")
    data['Enable'] = False
    data['Name'] = 'failed'
    data['GUID'] = 'failed'
if data['Enable']:
  printOK("Logging enabled")
else:
  printERROR("Logging set to '" + str(data['Enable']) + "'")
if (data['Name'] == "" or data['Name'] == "failed"):
  printERROR("Logging 'Name' not set - see " +  location)
  printERROR("GUID starts '" + data['GUID'][:13] + "'")
else:
  printOK ("Logging Name set to '" + data['Name'] + "'")
  printINFO("GUID starts '" + data['GUID'][:13] + "'")