import subprocess

def printTITLE(mystring):
  print ('-------')
  print ('\033[96m ' + mystring + '...\033[0m')
  print ('-------')

def printHEADER(mystring):
  print ('\033[95m ' + mystring + '...\033[0m')

def printOK(mystring):
  print ('\033[92m   OK - ' + mystring + '\033[0m')

def printWARNING(mystring):
  print ('\033[33m   WARNING - ' + mystring + '\033[0m')

def printERROR(mystring):
  print ('\033[91m   ERROR - ' + mystring + '\033[0m')

def printINFO(mystring):
  print ('\033[94m   INFO - ' + mystring + '\033[0m')

def runCommand(command):
  result = ""
  try:
    result = subprocess.check_output(command).decode('utf-8')
  except subprocess.CalledProcessError as e:
    printINFO("Command returned error code: " + str(e.returncode))
  return result