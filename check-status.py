#!/usr/bin/python3
from helper import *
from checks import *
import argparse

parser = argparse.ArgumentParser("checkstatus")
parser.add_argument("--latency", help="check the latency to each Relay node", required=False)
parser.add_argument("--speedtest", help="run speedtest", required=False)
args, leftovers = parser.parse_known_args()

preFlightChecks()
checkNode()
checkBalance()
checkResources()
checkPartKey()
checkLogging()
checkVersion()
checkConsensus()
if (args.latency is not None):
  checkLatencyTCP()
if (args.speedtest is not None):
  speedTest()