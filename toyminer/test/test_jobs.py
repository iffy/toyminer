from twisted.trial.unittest import TestCase


from toyminer.jobs import Job


class JobTest(TestCase):


    def test_init(self):
        job = Job('a'*40, 1, 100)
        self.assertEqual(job.given_hash, 'a'*40)
        self.assertEqual(job.difficulty, 1)
        self.assertEqual(job.scale, 100)
        self.assertEqual(job.miner, None)
        self.assertEqual(job.status, 'new')
        self.assertEqual(job.done.called, False)
        self.assertEqual(job.result, None)


    def test_changeStatus(self):
        """
        You can change the status of the job, which will notify other things
        """
        job = Job('a', 1, 100)
        called = []
        job.notifyOfChange(called.append)
        job.setStatus('foo')
        self.assertEqual(job.status, 'foo')
        self.assertEqual(called, [job])


    def test_changeMiner(self):
        """
        You can change the name of the miner doing the job
        """
        job = Job('a', 1, 100)
        called = []
        job.notifyOfChange(called.append)
        job.setMiner('foo')
        self.assertEqual(job.miner, 'foo')
        self.assertEqual(called, [job])


    def test_setResult(self):
        """
        Setting the result of a Job will call the done callback and set the
        result attribute.
        """
        job = Job('a', 1, 100)
        job.setResult('foo')
        self.assertEqual(self.successResultOf(job.done), job)
        self.assertEqual(job.result, 'foo')