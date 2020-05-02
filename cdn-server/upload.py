import os
import time
import traceback
from os.path import isfile

from tornado import gen
from tornado.web import RequestHandler

from messaging import Producer
from tasks import in_out

TEMP_ROOT = "/var/www/temp"
ARCHIVE_ROOT = "/var/www/archive"
KAFKA_TOPIC = "content_provider_sched"


class UploadHandler(RequestHandler):
    def post(self, *args, **kwargs):
        fileName = self.get_body_argument('fileName', None)
        file = self.request.files.get('file', None)
        uploadStatus = self.get_body_argument('uploadStatus', None)
        timeStamp = self.get_body_argument('timeStamp', None)
        count = self.get_body_argument('count', None)
        fileName = timeStamp + "-" + fileName
        proPath = os.path.join(TEMP_ROOT, fileName)
        if not os.path.isdir(proPath):
            os.makedirs(proPath)
        try:
            with open(os.path.join(proPath, count), 'wb') as f:
                f.write(file[0]['body'])
                self.set_status(200)
            if uploadStatus == 'end':
                in_out.delay(proPath, ARCHIVE_ROOT, fileName, count)
        except:
            self.set_status(401)
            print(traceback.format_exc(), flush=True)


class UploadOfflineHandler(RequestHandler):
    @gen.coroutine
    def post(self, *args, **kwargs):
        fileName = self.get_body_argument('fileName', None)
        file = self.request.files.get('file', None)
        uploadStatus = self.get_body_argument('uploadStatus', None)
        timeStamp = self.get_body_argument('timeStamp', None)
        count = self.get_body_argument('count', None)
        streamType = self.get_body_argument('type', "dash")
        fileName = timeStamp + "-" + fileName
        proPath = os.path.join(TEMP_ROOT, fileName)
        if not os.path.isdir(proPath):
            os.makedirs(proPath)
        try:
            with open(os.path.join(proPath, count), 'wb') as f:
                f.write(file[0]['body'])
                self.set_status(200)
            if uploadStatus == 'end':
                in_out.delay(proPath, ARCHIVE_ROOT, fileName, count)

                # schedule producing the stream
                stream = streamType + "/" + fileName + "/index." + ("m3u8" if streamType == "hls" else "mpd")
                print("request received to process offline stream: " + stream, flush=True)

                start_time = time.time()
                while time.time() - start_time < 10:
                    if isfile(ARCHIVE_ROOT + "/" + fileName):
                        print("file " + fileName + " exists, sending job", flush=True)
                        producer = Producer()
                        producer.send(KAFKA_TOPIC, stream)
                        producer.close()
                        return
                    yield gen.sleep(0.5)

                print("timeout :(", flush=True)
        except:
            self.set_status(401)
            print(traceback.format_exc(), flush=True)
