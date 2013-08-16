from twisted.trial.unittest import TestCase
from hashlib import sha1


from toyminer.solver import SyncMiner, validAnswer


class SyncMinerTest(TestCase):


    def test_works(self):
        h = sha1('foo').hexdigest()
        d = 1
        scale = 100
        r = SyncMiner().mine(h, d, scale)
        self.assertTrue(validAnswer(h, d, scale, r))


    def test_works_difficult(self):
        h = sha1('foo').hexdigest()
        d = 1
        s = 100000
        r = SyncMiner().mine(h, d, s)
        self.assertTrue(validAnswer(h, d, s, r))
