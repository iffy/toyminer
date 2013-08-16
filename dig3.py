# dig3.py
from twisted.internet import task, defer

from toyminer.proc import SubprocessMiner
from toyminer.jobs import Job
from toyminer.wrapper import NotifyingWrap
from toyminer.pool import MinerPool

import os

def change(job):
    print job

def showResult(job):
    print 'Result of %r: %r' % (job, job.result)

def main(reactor):
    pool = MinerPool()

    mine_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'mine.py')
    miner1 = NotifyingWrap(SubprocessMiner(mine_path), 'miner1')
    miner2 = NotifyingWrap(SubprocessMiner(mine_path), 'miner2')

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