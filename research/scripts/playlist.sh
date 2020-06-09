#!/bin/sh

curl -Ss --insecure "https://$HST/api/playlist?name=guest" | jq ".[]"
exit 0
