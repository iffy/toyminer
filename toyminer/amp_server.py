# toyminer/amp_server.py
from twisted.protocols import amp
from twisted.internet.protocol import Factory

from toyminer.wrapper import NotifyingWrap


class Mine(amp.Command):
    arguments = [('given_hash', amp.String()),
                 ('difficulty', amp.Integer()),
                 ('scale', amp.Integer())]
    response = [('answer', amp.String())]



class ServerProtocol(amp.AMP):

    num = 0

    def connectionMade(self):
        amp.AMP.connectionMade(self)
        ServerProtocol.num += 1
        num = ServerProtocol.num
        self.wrap = NotifyingWrap(self, 'AMPClient%d' % (num,))
        self.factory.pool.add(self.wrap)

    def mine(self, job):
        d = self.callRemote(Mine,
                given_hash=job.given_hash, difficulty=job.difficulty,
                scale=job.scale)
        return d.addCallback(lambda x:x['answer'])

    def connectionLost(self, reason):
        amp.AMP.connectionLost(self, reason)
        self.factory.pool.remove(self.wrap)


class ServerFactory(Factory):

    protocol = ServerProtocol

    def __init__(self, pool):
        """
        @param pool: A MinerPool instance that will have workers added to it
        """
        self.pool = pool

