# dig1.py
from twisted.internet import task, defer

from toyminer.sync import SyncMiner
from toyminer.jobs import Job
from toyminer.wrapper import NotifyingWrap
from toyminer.pool import MinerPool

def change(job):
    print job

def showResult(job):
    print 'Result of %r: %r' % (job, job.result)

def main(reactor):
    pool = MinerPool()

    miner1 = NotifyingWrap(SyncMiner(), 'miner1')
    miner2 = NotifyingWrap(SyncMiner(), 'miner2')

    pool.add(miner1)
    pool.add(miner2)

    jobs = [
        Job('a'*40, 1, 1000),
        Job('b'*40, 1, 10000),
        Job('c'*40, 1, 10000),
    ]
    for job in jobs:
        job.notifyOfChange(change)
        job.done.addCallback(showResult)

    return defer.gatherResults(map(pool.mine, jobs))

task.react(main)