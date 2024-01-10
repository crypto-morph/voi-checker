#!/usr/bin/bash
awk '/MemTotal/{t=$2}/MemAvailable/{a=$2}END{print 100-100*a/t}' /proc/meminfo
