from twisted.trial.unittest import TestCase
from twisted.internet import defer


from toyminer.jobs import Job
from toyminer.wrapper import NotifyingWrap

from toyminer.test.test_pool import FakeMiner



class NotifyingWrapTest(TestCase):


    @defer.inlineCallbacks
    def test_everything(self):
        miner = FakeMiner('result')
        wrapper = NotifyingWrap(miner, 'Jim')

        job = Job('a'*40, 1, 100)
        called = []
        job.notifyOfChange(called.append)

        r = yield wrapper.mine(job)
        self.assertEqual(job.miner, 'Jim')
        self.assertEqual(job.status, 'done')
        self.assertEqual(job.result.called, True)
        self.assertEqual(self.successResultOf(job.result), r)
        self.assertEqual(r, 'result')