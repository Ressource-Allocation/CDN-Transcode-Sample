#!/usr/bin/python3

import json

from tornado import web, gen

from streams import get_streams

ARCHIVE_ROOT = "/var/www/archive"


class PlayListHandler(web.RequestHandler):
    def __init__(self, app, request, **kwargs):
        super(PlayListHandler, self).__init__(app, request, **kwargs)
        self._cache = {}

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
