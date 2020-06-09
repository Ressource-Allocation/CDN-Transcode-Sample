#!/bin/bash

if [ $# -lt 2 ] || [ $# -gt 2 ];then
	echo "Incorrect number of parameters: $#"
	exit 1
fi

nb=$1
url=$2
c=0

while [ $c -lt "$nb" ];do
	vlc "https://$HST/$url" --no-video-deco --video-x=1 --video-y=1 --zoom=0.375 -L 2&>/dev/null &
	c=$((c + 1))
done

exit 0
