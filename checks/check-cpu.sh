#!/usr/bin/bash
(grep 'cpu ' /proc/stat;sleep 0.1;grep 'cpu ' /proc/stat)|awk -v RS="" '{print ($13-$2+$15-$4)*100/($13-$2+$15-$4+$16-$5)}'
