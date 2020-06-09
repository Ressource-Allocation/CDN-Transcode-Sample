#!/bin/sh

curl -Ss --insecure "https://$HST/clear/" | jq ".[]"
exit 0
