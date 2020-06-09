#!/bin/bash

if [ $# -lt 1 ] || [ $# -gt 1 ];then
	echo "Incorrect number of parameters: $#"
	exit 1
fi

case $1 in 
	"start")
		ssh "$USR"@"$HST" "mkdir ~/measures 2&>/dev/null && cd ~/measures && nmon -f -s1 -c6000"
		printf "Starting monitoring on %s." "$HST"
		;;
	"stop")
		ssh "$USR"@"$HST" "killall nmon"
		printf "Stopping monitoring on %s." "$HST"
		;;
	"download")
		scp -rp "$USR"@"$HST":~/measures .
		echo "Downloading measurement files."
		;;
	*)
		echo "Incorrect command: $1"
		exit 1
		;;
esac

exit 0
