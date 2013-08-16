from twisted.trial.unittest import TestCase
from twisted.internet import defer
from hashlib import sha1


from toyminer.threaded import ThreadedMiner
from toyminer.validate import validAnswer


class ThreadedMinerTest(TestCase):


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
