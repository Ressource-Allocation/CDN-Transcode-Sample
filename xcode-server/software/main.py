#!/usr/bin/python3

from os.path import isfile
from subprocess import call
from os import mkdir
from zkstate import ZKState
from messaging import Consumer
from abr_hls_dash import GetABRCommand
import traceback
import time

KAFKA_TOPIC = "content_provider_sched"
KAFKA_GROUP = "content_provider_dash_hls_creator"

ARCHIVE_ROOT = "/var/www/archive"
DASH_ROOT = "/var/www/dash"
HLS_ROOT = "/var/www/hls"


def process_stream(stream):
    # stream = "dash/video.mp4/index.mpd" or "hls/video.mp4/index.m3u8"
    print("process stream: " + stream, flush=True)

    stream_name = stream.split("/")[1]

    if not isfile(ARCHIVE_ROOT + "/" + stream_name):
        print("process aborted for stream name: " + stream_name, flush=True)
        return

    zk = ZKState("/content_provider_transcoder/" + ARCHIVE_ROOT + "/" + stream)
    # "/content_provider_transcoder/" + ARCHIVE_ROOT + "/" + stream
    # => "/content_provider_transcoder//var/www/archive/dash/video.mp4/index.mpd"
    # or "/content_provider_transcoder//var/www/archive/hls/video.mp4/index.m3u8"
    if zk.processed():
        print("process already done", flush=True)
        zk.close()
        return

    if stream.endswith(".mpd"):
        print("it's a dash process", flush=True)
        try:
            mkdir(DASH_ROOT + "/" + stream_name)
        except:
            pass

        if zk.process_start():
            try:
                cmd = GetABRCommand(ARCHIVE_ROOT + "/" + stream_name, DASH_ROOT + "/" + stream_name, "dash")
                r = call(cmd)
                if r:
                    raise Exception("status code: " + str(r))
                zk.process_end()
            except:
                print(traceback.format_exc(), flush=True)
                zk.process_abort()

    if stream.endswith(".m3u8"):
        print("it's a hls process", flush=True)
        try:
            mkdir(HLS_ROOT + "/" + stream_name)
        except:
            pass

        if zk.process_start():
            try:
                cmd = GetABRCommand(ARCHIVE_ROOT + "/" + stream_name, HLS_ROOT + "/" + stream_name, "hls")
                r = call(cmd)
                if r:
                    raise Exception("status code: " + str(r))
                zk.process_end()
            except:
                print(traceback.format_exc(), flush=True)
                zk.process_abort()

    zk.close()


if __name__ == "__main__":
    c = Consumer(KAFKA_GROUP)
    while True:
        try:
            for message in c.messages(KAFKA_TOPIC):
                print("new message received on topic " + KAFKA_TOPIC + ": " + message, flush=True)

                process_stream(message)
        except:
            print(traceback.format_exc(), flush=True)
            time.sleep(2)
    c.close()
