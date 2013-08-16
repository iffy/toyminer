# toyminer/threaded.py
from twisted.internet import threads
from toyminer.solver import mine

class ThreadedMiner(object):

    def mine(self, job):
        return threads.deferToThread(mine, job.given_hash, job.difficulty,
                                     job.scale)