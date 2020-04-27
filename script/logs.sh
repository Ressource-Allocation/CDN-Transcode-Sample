#!/bin/bash -e

if test -z "${DIR}"; then
    echo "This script should not be called directly."
    exit 1
fi

pid="$(sudo docker ps -f ancestor=$IMAGE --format='{{.ID}}' | head -n 1)"
if [ -n "$pid" ] && [ "$#" -le "1" ]; then
    echo "Logs from $IMAGE"
    sudo docker logs $pid
else
    echo "container $IMAGE not running"
fi

