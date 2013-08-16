# dig-amp.py
from twisted.internet import task, defer, endpoints
from twisted.python import log

from toyminer.amp_server import ServerFactory
from toyminer.jobs import Job
from toyminer.wrapper import NotifyingWrap
from toyminer.pool import MinerPool

import sys
import os

def change(job):
    print job

def showResult(job):
    print 'Result of %r: %r' % (job, job.result)

def main(reactor, amp_endpoint):
    log.startLogging(sys.stdout)
    pool = MinerPool()
    
    # start the AMP server
    amp_factory = ServerFactory(pool)
    amp_ep = endpoints.serverFromString(reactor, amp_endpoint)
    amp_ep.listen(amp_factory)

    jobs = [
        Job('a'*40, 1, 1000),
        Job('b'*40, 1, 10000),
        Job('c'*40, 1, 10000),
    ]
    for job in jobs:
        job.notifyOfChange(change)
        job.done.addCallback(showResult)

    return defer.gatherResults(map(pool.mine, jobs))

task.react(main, sys.argv[1:])