
import dns.resolver
from helper import *
import json
import multiprocessing
import os
import pkg_resources
import psutil
import re
import speedtest
from statistics import mean
import subprocess
from tcp_latency import measure_latency

def preFlightChecks():
  printHEADER("Pre-Flight-Checks")
  
  if (os.environ['addr'] == ""):
     printERROR("need to set \$addr before this script will work - run export addr=<YOUR VOI PARTICIPATION ACCOUNT>")
     exit()
     
  status, result = subprocess.getstatusoutput("goal")
  if (status != 0):
    printERROR('goal not found - check algorand package is installed and path is set')
    printERROR("won't go any further until that's available")
    exit()
  else:
    printINFO('goal command is present')
  
  required = {'psutil', 'speedtest-cli', 'statistics', 'tcp-latency'}
  installed = {pkg.key for pkg in pkg_resources.working_set}
  missing = required - installed
  
  if missing:
    printERROR(" ".join(missing) + ' is missing - run `pip install ' + " ".join(missing) + "` - see README for details")
  else:
    printINFO(" ".join(required) + ' are all installed')

def checkNode():
  printTITLE("VOI Participation Node Checker")
  printHEADER("Checking Node")
  addr = os.environ["addr"]
  printINFO("VOI address is " + addr)
  
  # First, check we are running VOI Swarm
  isSwarmEnabled = False
  isSwarmEnabled = swarmEnabled()
  
  # Second, check systemctl exists - if it doesn't we're probably not installed using D13s guide
  if (os.path.isfile('/usr/bin/systemctl')):
    printOK('systemctl detected (likely a D13 setup)')
  else:
    printWARNING('systemcl NOT detected - this checker only works with D13 setup (see Readme)')
  
  # Is the node running?
  if (os.path.isfile('/etc/supervisor/conf.d/supervisord.conf')):
    printWARNING('supervisord available - could be in a container - so no checking systemctl')
  else:
    checkactive = runCommand(["systemctl", "is-active", "voi"]).strip()
    if (checkactive == "active"):
      printOK("VOI Systemctl Node is started")
    elif (isSwarmEnabled):
      printOK("VOI Systemctl Node is not started - but Swarm VOI detected")
    else:
      printERROR("VOI Systemctl Node isn't started and Swarm VOI NOT detected")
  
  # Is the node synced?
  goal = runCommand(['goal','node','status'])
  goalcmd = re.search(r"Sync Time:\s+(\d+\.\d+)s",goal)
  if (float(goalcmd.group(1)) == 0.0):
    printOK("Node is in sync")
  else:
    printERROR("Node is out of sync - sync has been running for " + str(goalcmd.group(1)))
  
  # Is the node online?
  goal = runCommand(['goal','account','dump', '-a', addr ])
  goalcmd = re.search(r"\"onl\":\s+(\d+),",goal)
  if (int(goalcmd.group(1)) == 1):
    printOK("Node is in online")
  else:
    printERROR("Node is offline - status " + str(goalcmd.group(1)))
  
def checkBalance():
  lowVOI = 100 
  suggestedVOI = 550
  
  printHEADER("Checking Balance")
  
  goal = runCommand(["goal", "account", "dump", "-a", os.environ["addr"]])
  goalcmd = re.search(r"\"algo\"\:\s+(\d+)",goal)
  balance = int(goalcmd.group(1))
  
  if (balance >= (suggestedVOI * 1000000)):
    printOK(str(round(balance / 1000000,2)) + " VOI is enough")
  elif (balance <= (lowVOI * 1000000)): 
    printERROR(str(round(balance / 1000000,2)) + " VOI is a _lot_ less than optimal - add via the Discord faucet until you have more VOI until you have " + str(suggestedVOI))
  else:
    printWARNING(str(round(balance / 1000000,2)) + " VOI is less than optimal (" + str(suggestedVOI) +" or more)")

def checkResources():
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
    printOK("RAM usage is currently " + str(round(used_ram,2)) + "%")
  else:
    printERROR("RAM is high " + str(round(used_ram,2)) + "%")
  
  # HDD stats gathering
  
  available_disk = psutil.disk_usage('/').total /(1024.**3)
  percentage_used_disk = psutil.disk_usage('/').percent 
  
  printINFO('available space on / storage - ' + str(100 - percentage_used_disk) + "%")
  if (percentage_used_disk < highdisk):
    printOK("Root storage is " + str(round(percentage_used_disk,2)) + "%")
  else:
    printERROR("Root storage used is high " + str(round(percentage_used_disk,2)) + "%")

def checkPartKey():
  warningblocks = 5000
  testwarning = False
  testerror = False
  debug = False

  printHEADER("Checking Participation Key")
  
  # Goal participation key stats gathering 
  mylastround = 0
  
  goal = runCommand(['goal','node','lastround'])
  thisround = int(goal)
  if (thisround < 1):
    printERROR("Node not reporting last round")
  
  goal = runCommand(['goal','account','partkeyinfo'])
  goalcmd = re.findall(r"Effective last round:\s+(\d+)",goal)
  mylastround = 0
  if goalcmd is not None:
     mylastround = int(max(goalcmd))
  else:
     printERROR("Node not reporting Effective Last round")
  
  diff = mylastround - thisround
  
  if (testwarning):
    diff = warningblocks - 1
  if (testerror):
    diff = -10
  
  if (diff > warningblocks):
    printOK(str(diff) + " blocks until your key stops working")
  elif (diff > 0):
    printWARNING(str(diff) + " blocks until your key stops working")
  else:
    printERROR("Your key expired " + str(diff) + " blocks ago")

def checkLogging():

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

def versiontuple(v):
    return tuple(map(int, (v.split("."))))

def checkVersion():
  
  printHEADER("Check Versions")
  
  goal = runCommand(['goal','-v'])
  x = re.search(r"(\d+\.\d+\.\d+).stable",goal)
  version = x.group(1)
  
  printINFO("goal version - " + version)
  
  if (versiontuple(version) < versiontuple("3.21.0")):
    printERROR("This version " + version + " is less than 3.21.0 - some scripts may not run")
  
  goal = runCommand(['goal','-v'])
  x = re.search(r"(\d+\.\d+\.\d+).stable",goal)
  serverversion = x.group(1)
  
  printINFO("algod version - " + serverversion)
  if (serverversion != version):
    printERROR("version mismatch - server is " + str(serverversion) + ", goal is " + str(version))

def checkConsensus():
  
  printHEADER("Checking Consensus")
  addr = os.environ["addr"]
  avgPctOnTime = 0
  
  goal = runCommand(["curl", "-s", "https://analytics.testnet.voi.nodly.io/v0/consensus/accounts/all"])
  goalcmd = re.search(r"\s+\[\"" + addr + "\"\,\s+\"(\d+)\"\,\s+\"(\d+)\"\,\s+\"(\d+)\"\,\s+\"(\d+)\"\,\s+(\d+)\,\s+\"(\d+)\"\,\s+\"([^,]+)\"\,\s+([^,]+),\s+([^,]+),\s+(.+)\]\,",goal)
  if goalcmd is not None: 
    avgPctOnTime = float(goalcmd.group(10))
  else:
    printERROR('Checker failed to get find consensus output from analytics.testnet.voi.nodly.io - could take a while to turn up if you have just started the node')
  if (avgPctOnTime > 80):
    printOK("good average percentage on time - " + str(avgPctOnTime) + "%")
  else: 
    printWARNING("low average percentage on time - " + str(avgPctOnTime) + "%")

def ping(myhost: str, myip: str, myport: int = 5011, myruns: int = 5) -> float:
     latency = measure_latency(host=myip, port=myport, runs=myruns)
     if(not latency):
       printERROR('{0}({1}) returned no response on port {2} (tried {3} times)'.format(myhost,myip,myport, myruns))
       return 10000
     else:
       printINFO("checking {0}...{1}".format(myhost,str(round(mean(latency),2)) + "ms"))
       return mean(latency)
  
def checkLatencyTCP():
    
  # counters
  region = {}
  regioncount = {}
  errorscount = 0
  ips = []
  
  # init
  resolver = dns.resolver.Resolver()
  resolver.nameservers = ["8.8.8.8"]  # use Google's DNS server
  
  # check the latency of each ip
  
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

def speedTest():
  printHEADER("Running Internet Speed Test")
  
  threads = None
  servers = []
  s = speedtest.Speedtest()
  s.get_servers(servers)
  s.get_best_server()
  s.download(threads=threads)
  s.upload(threads=threads)
  s.results.share()


  #print(json.dumps(s.results.dict(),indent=2))
  j = json.loads(json.dumps(s.results.dict()))
  print("Client Latency {} ms".format(round(j['ping'],2)))
  print("Download {} Mbps".format(round(j['download']/1000000,2)))
  print("Upload {} Mbps".format(round(j['upload']/1000000,2)))
  print("Latency {} ms".format(round(j['server']['latency'],2)))
  
  