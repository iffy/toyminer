# toyminer/sync.py
from toyminer.solver import mine

class SyncMiner(object):

    def mine(self, job):
        return mine(job.given_hash, job.difficulty, job.scale)
