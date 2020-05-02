#!/usr/bin/python3
from os import listdir

from zkstate import ZKState

ARCHIVE_ROOT = "/var/www/archive"
BASE_PATH = "/content_provider_transcoder/" + ARCHIVE_ROOT + "/"


def get_streams():
    try:
        available_videos = [f for f in listdir(ARCHIVE_ROOT) if f.endswith((".mp4", ".avi"))]
    except:
        return None

    streams_dict = []
    types = [("hls", ".m3u8"), ("dash", ".mpd")]
    for f in available_videos:
        for t in types:
            url = t[0] + "/" + f + "/index" + t[1]
            zk = ZKState(BASE_PATH + url)
            streams_dict.append({
                "name": t[0] + "-" + f,
                "url": url,
                "img": "thumbnail/" + f + ".png",
                "type": t[0],
                "file": f,
                "zk": {
                    "path": zk.get_path(),
                    "state": zk.get_state()
                }
            })

    return streams_dict
