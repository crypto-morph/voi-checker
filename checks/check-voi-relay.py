#!/usr/bin/python3
import dns.resolver
import subprocess
import re
from helper import *

def ping(host: str, timeout: int = 500) -> float:
   myhost = str(host.strip("."))
   ping = subprocess.Popen("ping " + str(myhost) + " -c 5", stdout = subprocess.PIPE,stderr = subprocess.PIPE, shell=True)
   output = str(ping.communicate())
   if ('100% packet loss' in output):
     printERROR("ping {0} failed - ignore in stats".format(myhost))
     return 10000
   elif ('Name or service not known' in output):
      printERROR("unable to resolve {0} - ignore in stats".format(myhost))
      return 10001
   else:
     pattern = r"rtt min/avg/max/mdev = \d+\.\d+/(\d+\.\d+)"
     return re.findall(pattern, output)[0]

printHEADER("Checking Relay Latency (this could take a few moments)")
ips = []
resolver = dns.resolver.Resolver()
resolver.nameservers = ["8.8.8.8"]  # use Google's DNS server
try:
    answers = resolver.resolve("_algobootstrap._tcp.voitest.voi.network", "SRV")
except dns.resolver.NoAnswer:
    printERROR('Failed to lookup relay names')

region = {}
regioncount = {}

for rdata in answers:
    host = str(rdata.target)
    myregion, mynumber = re.findall("r\-(\w+)\-(\d+)", host)[0]
    latency = ping(host)
    if(latency != 10000 and latency !=10001):
      region[myregion] = region.get(myregion,0.0) + float(latency)
      regioncount[myregion] = regioncount.get(myregion,0) + 1
      printINFO("checking {0}...{1}".format(host,str(latency) + "ms"))

printHEADER("Results...")

print("\tRegion\t|\tAvg Latency\t")
for key in region:
   print("\t{0}\t|\t{1}\t".format(key,region[key]/regioncount[key]))