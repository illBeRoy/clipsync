import beacon

from twisted.internet import threads, task


class Discovery(object):

    def __init__(self, beacon_server, beacon_client, discovery_port, discovery_keyword):
        self._beacon_server = beacon_server
        self._beacon_client = beacon_client
        self._discovery_port = discovery_port
        self._discovery_keyword = discovery_keyword
        self._peers = []

    @property
    def peers(self):
        return self._peers

    def start(self):
        self._start_beacon()
        self._start_listening()

    def _start_beacon(self):
        self._beacon_server.start()

    def _start_listening(self):
        task.LoopingCall(threads.deferToThread, self._peers_update).start(1.0)

    def _peers_update(self):
        peers = self._beacon_client.find_all_servers(self._discovery_port, self._discovery_keyword)
        self._peers = [peer for peer in peers if peer not in ['localhost', '127.0.0.1']]

    @staticmethod
    def create(args=None):
        discovery_port = 12000
        discovery_keyword = 'clipsync'

        beacon_server = beacon.Beacon(discovery_port, discovery_keyword)
        beacon_server.daemon = True

        return Discovery(beacon_server, beacon, discovery_port, discovery_keyword)
