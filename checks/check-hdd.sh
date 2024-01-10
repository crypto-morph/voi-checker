#!/usr/bin/bash
df | awk '/ \/$/{print $5}'

