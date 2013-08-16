#!/usr/bin/env python
# launchampclient.py
from twisted.internet import task, endpoints, defer
from twisted.python import log

from toyminer.proc import SubprocessMiner
from toyminer.amp_client import MinerProtocol

import sys
import os

def main(reactor, endpoint):
    """
    Connect to a server to volunteer for work.
    """
    log.startLogging(sys.stdout)
    
    # get the miner ready
    mine_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'mine.py')
    proto = MinerProtocol(SubprocessMiner(mine_path))

    # connect the miner to the server
    client_endpoint = endpoints.clientFromString(reactor, endpoint)
    endpoints.connectProtocol(client_endpoint, proto)
    return proto.done


if __name__ == '__main__':
    import sys
    task.react(main, sys.argv[1:])
