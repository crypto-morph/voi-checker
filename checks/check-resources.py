#!/usr/bin/python3
import re
from helper import *

highcpu = 80;
highram = 80;
highhd = 95;

printHEADER("Check Resources")

# CPU stats gathering 

cpucmd = re.search(r"(\d+)",runCommand(['checks/check-cpu.sh']))
cpu = int(cpucmd.group(1))
if (cpu < highcpu):
  printOK("CPU - " + str(cpu) + "%")
else:
  printERROR("CPU is high - " + str(cpu) + "%")

# RAM stats gathering

ramcmd = re.search(r"(\d+)",runCommand(['checks/check-mem.sh']))
ram = int(ramcmd.group(1))
if (ram < highram):
  printOK("RAM - " + str(ram) + "%")
else:
  printERROR("RAM is high - " + str(ram) + "%")

# HDD stats gathering

hddcmd = re.search(r"(\d+)",runCommand(['checks/check-hdd.sh']))
hdd = int(hddcmd.group(1))
if (hdd < highhd):
  printOK("HDD - " + str(hdd) + "%")
else:
  printERROR("HDD is high - " + str(hdd) + "%")

#$hd = `checks/check-hdd.sh`;
#chomp($hd);
#chop($hd); # remove %
#if ($hd < $highhd)
#{
#  print GREEN "OK ($hd\%)\n" . RESET;
#}
#else
#{
#  print RED "HD usage is high ($hd\%)\n" . RESET;
#}	
#