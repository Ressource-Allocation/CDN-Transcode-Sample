#!/usr/bin/python3

from tornado import web, gen

ARCHIVE_ROOT = "/var/www/archive"


class ClearHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        self.set_status(200, "OK")
        self.set_header("Content-Type", "text/html")
        self.write("Deletion in progress.")
