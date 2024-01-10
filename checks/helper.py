import subprocess

def printHEADER(mystring):
  print ('\033[95m ' + mystring + '...\033[0m')

def printOK(mystring):
  print ('\033[92m OK - ' + mystring + '\033[0m')

def printERROR(mystring):
  print ('\033[91m ERROR - ' + mystring + '\033[0m')

def printINFO(mystring):
  print ('\033[94m INFO - ' + mystring + '\033[0m')

def runCommand(command):
  return subprocess.check_output(command).decode('utf-8')
