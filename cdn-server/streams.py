#!/usr/bin/python3
from os import listdir

from tornado import web, gen
import json
from zkstate import ZKState

ARCHIVE_ROOT = "/var/www/archive"
DASH_ROOT = "/var/www/dash"
HLS_ROOT = "/var/www/hls"
BASE_PATH = "/content_provider_transcoder/" + ARCHIVE_ROOT + "/"


def get_streams():
    try:
        dash_streams_folders = [f for f in listdir(DASH_ROOT)]
        hls_streams_folders = [f for f in listdir(HLS_ROOT)]
    except:
        return None

    dashls_streams_dict = []
    for f in dash_streams_folders:
        zk = ZKState(BASE_PATH + "dash/" + f + "/index.mpd")
        dashls_streams_dict.append({
            "type": "dash",
            "file": f,
            "zk": {
                "path": zk.get_path(),
                "state": "Pending" if zk.processed() is None else "Processed"
            }
        })
    for f in hls_streams_folders:
        zk = ZKState(BASE_PATH + "hls/" + f + "/index.m3u8")
        dashls_streams_dict.append({
            "type": "hls",
            "file": f,
            "zk": {
                "path": zk.get_path(),
                "state": "Pending" if zk.processed() is None else "Processed"
            }
        })

    return dashls_streams_dict


class StreamsHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        streams = get_streams()

        if streams is None:
            print("Error while parsing folders", flush=True)
            self.set_status(500, "Internal Error")
            return

        self.set_status(200, "OK")
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(streams))
