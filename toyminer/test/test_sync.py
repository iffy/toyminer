from twisted.trial.unittest import TestCase
from hashlib import sha1


from toyminer.sync import SyncMiner
from toyminer.jobs import Job
from toyminer.validate import validAnswer


class SyncMinerTest(TestCase):


    def test_works(self):
        h = sha1('foo').hexdigest()
        d = 1
        scale = 100
        job = Job(h, d, scale)
        r = SyncMiner().mine(job)
        self.assertTrue(validAnswer(h, d, scale, r))


    def test_works_difficult(self):
        h = sha1('foo').hexdigest()
        d = 1
        s = 100000
        r = SyncMiner().mine(Job(h, d, s))
        self.assertTrue(validAnswer(h, d, s, r))
