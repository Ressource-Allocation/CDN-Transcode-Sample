#!/bin/bash

if [ $# -lt 1 ] || [ $# -gt 1 ];then
	echo "Incorrect number of parameters: $#"
	exit 1
fi

file="$1.times"
date >> "$file"

exit 0
