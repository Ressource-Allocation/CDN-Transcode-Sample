#!/usr/bin/python3
import json
import traceback

from kazoo.client import KazooClient
from kazoo.exceptions import NodeExistsError

ZK_HOSTS = 'zookeeper-service:2181'


class ZKState(object):
    def __init__(self, path, name=None):
        super(ZKState, self).__init__()
        options = {"max_tries": -1, "max_delay": 5, "ignore_expire": True}
        self._zk = KazooClient(hosts=ZK_HOSTS, connection_retry=options)
        try:
            self._zk.start(timeout=3600)
        except:
            print(traceback.format_exc(), flush=True)
        self._path = path
        self._name = "" if name is None else name + "."
        self._zk.ensure_path(path)

    def processed(self):
        """Check if the stream has been processed.

        :returns: ZnodeStat of the stream if it is processed, else None.
        :rtype: :class:`~kazoo.protocol.states.ZnodeStat` or `None`.

        :raises:
            :exc:`~kazoo.exceptions.ZookeeperError` if the server
            returns a non-zero error code.

        """
        return self._zk.exists(self._path + "/" + self._name + "complete")

    def process_start(self):
        if self.processed():
            return False
        try:
            self._zk.create(self._path + "/" + self._name + "processing", ephemeral=True)
            return True
        except NodeExistsError:  # another process wins
            return False

    def process_end(self):
        try:
            self._zk.create(self._path + "/" + self._name + "complete")
        except NodeExistsError:
            pass

    def process_abort(self):
        # the ephemeral node will be deleted upon close
        pass

    def close(self):
        self._zk.stop()
        self._zk.close()

    def clear(self):
        """Delete the stream from ZK

        :returns: True if it succeeded, False if failed or if the
                  stream was not yet processed
        :rtype: bool

        """
        if self.processed():
            self._zk.delete(self._path + "/" + self._name + "complete")
            return self.processed() is None
        return False

    def to_json(self):
        return json.dumps({"path": self._path})

    def get_path(self):
        return self._path
