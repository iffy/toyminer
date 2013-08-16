from twisted.trial.unittest import TestCase
from twisted.internet import defer


from toyminer.jobs import Job
from toyminer.pool import MinerPool


class FakeMiner(object):

    def __init__(self, retval=None):
        self.called = []
        self.retval = retval

    def mine(self, job):
        self.called.append(job)
        return self.retval




class MinerPoolTest(TestCase):

    timeout = 3

    @defer.inlineCallbacks
    def test_addAndMine(self):
        """
        You can add miners to the pool and then use them to mine
        """
        pool = MinerPool()
        m1 = FakeMiner('foo')
        pool.add(m1)
        j1 = Job('a'*40, 1, 100)
        result = yield pool.mine(j1)
        self.assertEqual(result, 'foo')
        self.assertEqual(m1.called, [j1])
        j2 = Job('a'*40, 1, 200)
        r2 = yield pool.mine(j2)
        self.assertEqual(r2, 'foo')
        self.assertEqual(m1.called, [j1, j2])



    @defer.inlineCallbacks
    def test_remove(self):
        """
        You can remove miners from the pool
        """
        pool = MinerPool()
        m1 = FakeMiner('foo')
        m2 = FakeMiner(defer.Deferred())
        pool.add(m1)
        pool.add(m2)

        miners = pool.listMiners()
        self.assertEqual(set(miners), set([m1, m2]))

        # straightforward remove
        r = yield pool.remove(m1)
        self.assertEqual(r, m1)
        miners = pool.listMiners()
        self.assertEqual(set(miners), set([m2]))

        # remove while miner is doing a job should wait until the miner is done
        j1 = Job('a', 1, 100)
        r = pool.mine(j1)
        self.assertEqual(r.result, m2.retval, "should not have finished the job")
        rm_d = pool.remove(m2)

        miners = pool.listMiners()
        self.assertEqual(miners, [m2], "Should still be listed because it's not"
                         " removed yet")

        m2.retval.callback('hey')
        self.assertEqual(self.successResultOf(r), 'hey')
        self.assertEqual(self.successResultOf(rm_d), m2)
        self.assertEqual(pool.listMiners(), [])

        m2.retval = defer.succeed('hey')
        pool.add(m2)
        j2 = Job('a', 1, 100)
        r = yield pool.mine(j2)
        self.assertEqual(r, 'hey')

