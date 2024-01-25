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
2) `./check-status.sh`

If you would like to add an optional Bandwidth test (using "speedtest cli") you can run like this:

`./check-status.sh bandwidth`

There is also an experimental latency check mode - this connects to all the active Relays one at a time and measures the time it takes by region. 

`./check-status.sh tcplatency`

## Example output

```
----
VOI Participation Node Checker
----
address is set to TG4XRUVGGQZOS6JYNRFN5EWBL2ZKWKZHIOIC2OKURX3FPFYKFCYJ7X44M4
----
Checking if node is started... OK
Checking if node is in sync... IN SYNC
Checking if Node believes it is online... ONLINE
Checking balance... OK - 569.989 voi is enough
Checking machine resources...
  CPU... OK (0.60241%)
  RAM... OK (6.46636%)
  HDD... OK (3%)
```
