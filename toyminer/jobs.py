# toyminer/jobs.py
from twisted.internet import defer


class Job(object):
    """
    I am a mining request.
    """

    miner = None
    status = 'new'
    result = None

    def __init__(self, given_hash, difficulty, scale):
        self.given_hash = given_hash
        self.difficulty = difficulty
        self.scale = scale
        self.done = defer.Deferred()
        self._funcs_to_notify = []


    def __repr__(self):
        return '<Job %s %s %s %r %r>' % (self.status, self.miner,
                                         self.given_hash[:7], self.difficulty,
                                         self.scale)


    def notifyOfChange(self, callback):
        """
        Register a function to be called when things on this job change.
        """
        self._funcs_to_notify.append(callback)


    def _notify(self):
        for func in self._funcs_to_notify:
            func(self)


    def setStatus(self, status):
        """
        Set the status of this job, and notify things that care.
        """
        self.status = status
        self._notify()


    def setMiner(self, name):
        """
        Set the name of the miner doing this job and notify things that care.
        """
        self.miner = name
        self._notify()


    def setResult(self, result):
        """
        Set the result and notify things that care.
        """
        self.result = result
        self.done.callback(self)
        self._notify()