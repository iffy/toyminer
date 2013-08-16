# toyminer/wrapper.py
from twisted.internet import defer

class NotifyingWrap(object):
    """
    I am a miner that wraps another miner and tells the Job what's going on.
    """

    def __init__(self, miner, name):
        self.name = name
        self.miner = miner


    def mine(self, job):
        job.setMiner(self.name)
        job.setStatus('running')
        d = defer.maybeDeferred(self.miner.mine, job)
        d.addBoth(self._doneMining, job)
        return d


    def _doneMining(self, result, job):
        job.setResult(result)
        job.setStatus('done')
        return result