#!/bin/bash
if [[ $addr == "" ]]; then
  echo "need to set \$addr before this script will work - run export addr=<YOUR VOI PARTICIPATION ACCOUNT>"
else
  ./checks/check-node.py
  ./checks/check-balance.py
  ./checks/check-resources.py
  ./checks/check-partkey.py
  ./checks/check-logging.py
  ./checks/check-version.py
  ./checks/check-consensus.py
fi