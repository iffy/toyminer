# toyminer/threaded.py
from twisted.internet import threads
from toyminer.sync import SyncMiner

class ThreadedMiner(object):

    def __init__(self):
        self._miner = SyncMiner()

    def mine(self, job):
        return threads.deferToThread(self._miner.mine, job)