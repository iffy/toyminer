from twisted.trial.unittest import TestCase
from twisted.internet import defer
from hashlib import sha1


from toyminer.threaded import ThreadedMiner
from toyminer.jobs import Job
from toyminer.validate import validAnswer


class ThreadedMinerTest(TestCase):

    timeout = 3

    @defer.inlineCallbacks
    def test_works(self):
        h = sha1('foo').hexdigest()
        d = 1
        scale = 100
        r = yield ThreadedMiner().mine(Job(h, d, scale))
        self.assertTrue(validAnswer(h, d, scale, r))


    @defer.inlineCallbacks
    def test_works_difficult(self):
        h = sha1('foo').hexdigest()
        d = 1
        s = 100000
        r = yield ThreadedMiner().mine(Job(h, d, s))
        self.assertTrue(validAnswer(h, d, s, r))
