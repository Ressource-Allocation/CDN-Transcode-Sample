#!/usr/bin/python3

import os

from tornado import ioloop, web
from tornado.options import define, options, parse_command_line

from clear import ClearHandler
from playlist import PlayListHandler
from schedule import ScheduleHandler
from upload import UploadHandler, UploadOfflineHandler

APP = web.Application([
    (r'/playlist', PlayListHandler),
    (r'/schedule/.*', ScheduleHandler),
    (r'/upload/', UploadHandler),
    (r'/upload-offline/', UploadOfflineHandler),
    (r'/clear/', ClearHandler),
])

if __name__ == "__main__":
    define("port", default=2222, help="the binding port", type=int)
    define("ip", default="127.0.0.1", help="the binding ip")
    parse_command_line()
    os.popen('celery multi start w1 -A tasks -l info --logfile=/var/www/log/celery.log --pidfile=/var/www/celery.pid')
    print("Listening to " + options.ip + ":" + str(options.port))
    APP.listen(options.port, address=options.ip)
    ioloop.IOLoop.instance().start()
