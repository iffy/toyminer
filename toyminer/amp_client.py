# toyminer/amp_client.py
from twisted.protocols import amp
from twisted.internet import defer

from toyminer.jobs import Job
from toyminer.amp_server import Mine


class MinerProtocol(amp.AMP):

    def __init__(self, miner):
        amp.AMP.__init__(self)
        self.miner = miner
        self.done = defer.Deferred()

    @Mine.responder
    def doMining(self, given_hash, difficulty, scale):
        job = Job(given_hash, difficulty, scale)
        d = self.miner.mine(job)
        return d.addCallback(lambda x:{'answer':x})

    def connectionLost(self, reason):
        amp.AMP.connectionLost(self, reason)
        self.done.callback(self)
