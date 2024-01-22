#!/usr/bin/python3
import dns.resolver
import re
from statistics import mean
from tcp_latency import measure_latency
from helper import *

# counters
region = {}
regioncount = {}
errorscount = 0
ips = []

# init
resolver = dns.resolver.Resolver()
resolver.nameservers = ["8.8.8.8"]  # use Google's DNS server

# check the latency of each ip

def ping(myhost: str, myip: str, myport: int = 5011, myruns: int = 5) -> float:
   latency = measure_latency(host=myip, port=myport, runs=myruns)
   if(not latency):
     printERROR('{0}({1}) returned no response on port {2} (tried {3} times)'.format(myhost,myip,myport, myruns))
     return 10000
   else:
     printINFO("checking {0}...{1}".format(myhost,str(round(mean(latency),2)) + "ms"))
     return mean(latency)

# Start here

printHEADER("Checking Relay Latency (this could take a few moments)")
try:
    answers = resolver.resolve("_algobootstrap._tcp.voitest.voi.network", "SRV")
except dns.resolver.NoAnswer:
    printERROR('Failed to lookup relay names')

for rdata in answers:
  myhost = str(rdata.target).strip(".")
  myregion, mynumber = re.findall("r\-([a-zA-Z]+)\-(\d+)", myhost)[0]
  try:
    data = resolver.resolve(str(rdata.target), "A")
  except dns.resolver.NoAnswer:
    printERROR('No answer from DNS server {0}'.format(myhost))
  except dns.resolver.LifetimeTimeout:
    printERROR('DNS server timed out when asked about {0}'.format(myhost))
  except dns.resolver.NXDOMAIN:
    printERROR('Non-existant domain {0}'.format(myhost))
  for a in data:
    myip = str(a)
  mylatency = ping(myhost,myip)
  if(mylatency != 10000 and mylatency !=10001):
    region[myregion] = region.get(myregion,0.0) + float(mylatency)
    regioncount[myregion] = regioncount.get(myregion,0) + 1
  else:
    errorscount += 1

# print out results
    
printHEADER("Results...")

print("\tRegion\t|\tAvg Latency\t")
for key in region:
   print("\t{0}\t|\t{1}\t".format(key,round(region[key]/regioncount[key],2)))
print("Errors = {0}".format(errorscount))