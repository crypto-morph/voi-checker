# VOI Participation Node Checker

by Morph42

A collection of scripts for quickly finding the status of your VOI node.
These scripts should work on any node setup using D13s instructions - https://d13.co/posts/set-up-voi-participation-node/.

## Prerequisites

1) Check you have set your VOI wallet address in your environment:
   `export addr=<VOI WALLET ADDRESS>`
2) Clone the repo to your node:
   `git clone https://github.com/crypto-morph/voi-checker.git`
3) Ensure you have pip installed:
   `sudo apt install pip`
4) Ensure you have the required modules installed:
   `pip install -r requirements.txt`

## Usage

1) `cd voi-checker`
2) `./check-status.py`

If you would like to add an optional Bandwidth test (using "speedtest cli") you can run like this:

`./check-status.py --speedtest=true`

There is also an experimental latency check mode - this connects to all the active Relays one at a time and measures the time it takes by region. 

`./check-status.py --latency=true`

## Example output

```
$ ./check-status.sh 
 Pre-Flight-Checks...
   INFO - goal command is present
   INFO - speedtest-cli statistics psutil tcp-latency are all installed
-------
 VOI Participation Node Checker...
-------
 Checking Node...
   INFO - VOI address is XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   OK - systemctl detected (likely a D13 setup)
   OK - VOI Node is started
   OK - Node is in sync
   OK - Node is in online
 Checking Balance...
   OK - 550 VOI is enough
 Check Resources...
   INFO - uptime is 20.49 days
   INFO - The CPU usage is : 8.67
   INFO - Logical CPU Count is 16
   INFO - Actual CPU Count is 8
   OK - CPU usage is currently 8.67%
   INFO - RAM present is 28.29Gb
   INFO - Used RAM present is 8.91Gb
   OK - RAM usage is currently 8.908443450927734%
   INFO - available space on / storage - 94.0%
   OK - Root storage is 6.0%
 Checking Participation Key...
   OK - 1192643 blocks until your key stops working
 Checking Logging...
   OK - Logging enabled
   OK - Logging Name set to 'XXXXXXXX'
   INFO - GUID starts 'XXXXXXXX-XXXX'
 Check Versions...
   INFO - goal version - 3.21.0
   INFO - algod version - 3.21.0
 Checking Consensus...
   OK - good average percentage on time - 96.6%
```
Latency check:
```
 Checking Relay Latency (this could take a few moments)...
   INFO - checking r-na-39.testnet.voi.network...143.56ms
   ERROR - r-na-25.testnet.voi.network(15.204.233.209) returned no response on port 5011 (tried 5 times)
   INFO - checking r-apac-07.testnet.voi.network...283.0ms
   INFO - checking r-eu-18.testnet.voi.network...33.17ms
   INFO - checking r-eu-53.testnet.voi.network...51.64ms
   INFO - checking r-eu-21.testnet.voi.network...28.1ms
   INFO - checking r-apc-15.testnet.voi.network...243.44ms
   ...snip...
   
```