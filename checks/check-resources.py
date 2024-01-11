#!/usr/bin/python3
import os
import re
import multiprocessing
from helper import *

highcpu = 80;
highram = 80;
highhd = 95;

printHEADER("Check Resources")

# Gather uptime

with open('/proc/uptime', 'r') as f:
  uptime_seconds = float(f.readline().split()[0])
  uptime_days = round(uptime_seconds / 60 / 60 / 24,2)

printINFO("uptime is " + str(uptime_days) + " days")



# CPU stats gathering 

printINFO("CPU Count is " + str(multiprocessing.cpu_count()))

cpucmd = re.search(r"(\d+)",runCommand(['checks/check-cpu.sh']))
cpu = int(cpucmd.group(1))
if (cpu < highcpu):
  printOK("CPU usage is currently - " + str(cpu) + "%")
else:
  printERROR("CPU is high - " + str(cpu) + "%")

# RAM stats gathering

mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')  # e.g. 4015976448
mem_gib = mem_bytes/(1024.**3)

printINFO("RAM present is " + str(mem_gib) + "Gb")

ramcmd = re.search(r"(\d+)",runCommand(['checks/check-mem.sh']))
ram = int(ramcmd.group(1))
if (ram < highram):
  printOK("RAM usage is currently " + str(ram) + "%")
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