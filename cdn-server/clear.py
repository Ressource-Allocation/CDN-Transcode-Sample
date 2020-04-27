#!/usr/bin/python3

from subprocess import call
from typing import NewType

from tornado import web, gen
import json
from zkstate import ZKState
from streams import get_streams

ARCHIVE_ROOT = "/var/www/archive"
DASH_ROOT = "/var/www/dash"
HLS_ROOT = "/var/www/hls"
BASE_PATH = "/content_provider_transcoder/" + ARCHIVE_ROOT + "/"
ZkType = NewType('ZkType', ZKState)


class ClearHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        streams = get_streams()
        if streams is None:
            print("Error while parsing folders", flush=True)
            self.set_status(500, "Internal Error")
            return

        for s in streams:
            zk = ZKState(s["zk"]["path"])
            if zk.clear():
                root = DASH_ROOT if s["type"] == "dash" else HLS_ROOT
                r = call(["rm", "-rf", root + "/" + s["file"]])
                if r != 0:
                    print("Failed to rm: " + s["zk"]["path"], flush=True)
                    s["zk"]["state"] = "Failed"
                else:
                    s["zk"]["state"] = "Cleared"
            else:
                print("Failed to clear or not processed: " + s["zk"]["path"], flush=True)
                s["zk"]["state"] = "Failed"

        self.set_status(200, "OK")
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(streams))
