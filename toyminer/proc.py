# toyminer/proc.py
from twisted.internet.utils import getProcessOutput

class SubprocessMiner(object):

    def __init__(self, path):
        self.path = path

    def mine(self, job):
        args = [job.given_hash, str(job.difficulty), str(job.scale)]
        return getProcessOutput(self.path, args)
