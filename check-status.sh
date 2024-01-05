#!/bin/bash
DEBUG=1
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -n "Checking if node is started..."
if systemctl is-active voi | grep -q 'inactive'; then printf "${RED} Node not started ${NC}\n"; else printf  "${GREEN} OK ${NC}\n"; fi
echo -n  "Checking if node is in sync..."
if goal node status | grep -q 'Sync Time: 0.0s'; then printf "${GREEN} IN SYNC ${NC}\n"; else printf "${RED} node is not in sync ${NC}\n"; fi
echo -n "Checking if Node believes it is online..."
if goal account dump -a $addr | grep -q '"onl": 1,'; then printf "${GREEN} ONLINE ${NC}\n"; else printf "${RED} You are offline ${NC}\n"; fi

