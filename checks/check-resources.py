#!/usr/bin/python3
import os
import re
import multiprocessing
import psutil
from helper import *
 
highcpu = 80;
highram = 80;
highdisk = 95;

printHEADER("Check Resources")

# Gather uptime

with open('/proc/uptime', 'r') as f:
  uptime_seconds = float(f.readline().split()[0])
  uptime_days = round(uptime_seconds / 60 / 60 / 24,2)

printINFO("uptime is " + str(uptime_days) + " days")

# CPU stats gathering 

load1, load5, load15 = psutil.getloadavg()
cpu_usage = (load15/os.cpu_count()) * 100
cpu_count = psutil.cpu_count(logical=False)
logical_cpu_count =  psutil.cpu_count(logical=True)

printINFO("The CPU usage is : " + str(round(cpu_usage,2)))
printINFO("Logical CPU Count is " + str(logical_cpu_count))
printINFO("Actual CPU Count is " + str(cpu_count))
if (cpu_usage < highcpu):
  printOK("CPU usage is currently " + str(round(cpu_usage,2)) + "%")
else:
  printERROR("CPU is high at " + str(cpu_usage) + "%")

# RAM stats gathering

mem_gib = psutil.virtual_memory().total /(1024.**3)
printINFO("RAM present is " + str(round(mem_gib,2)) + "Gb")

used_ram = psutil.virtual_memory().used /(1024.**3)
printINFO("Used RAM present is " + str(round(used_ram,2)) + "Gb")

if (used_ram < highram):
  printOK("RAM usage is currently " + str(used_ram) + "%")
else:
  printERROR("RAM is high " + str(used_ram) + "%")

# HDD stats gathering

available_disk = psutil.disk_usage('/').total /(1024.**3)
percentage_used_disk = psutil.disk_usage('/').percent 

printINFO('available space on / storage - ' + str(100 - percentage_used_disk) + "%")
if (percentage_used_disk < highdisk):
  printOK("Root storage is " + str(round(percentage_used_disk,2)) + "%")
else:
  printERROR("Root storage used is high " + str(round(percentage_used_disk,2)) + "%")
