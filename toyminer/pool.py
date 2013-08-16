# toyminer/pool.py
from twisted.internet import defer


class MinerPool(object):
    """
    I am a mid-level manager.  I don't do any mining, but I send jobs off to
    the miners in my queue.
    """


    def __init__(self):
        self.queue = defer.DeferredQueue()
        self.all_miners = []
        self._to_remove = []


    def mine(self, job):
        """
        Choose a miner from the pool, and have them mine
        """
        d = self.queue.get()
        d.addCallback(self._mineWithMiner, job)
        return d


    def _mineWithMiner(self, miner, job):
        """
        Have the specified miner mine, then return the miner to the pool when
        done.
        """
        d = defer.maybeDeferred(miner.mine, job)
        return d.addBoth(self._returnToQueue, miner)


    def _returnToQueue(self, result, miner):
        """
        Return the miner to the pool, then pass along the result of the
        mining.
        """
        # see if it has been requested to remove this miner
        for i, tup in enumerate(self._to_remove):
            if tup[0] == miner:
                self.all_miners.remove(miner)
                del self._to_remove[i]
                tup[1].callback(miner)
                break
        else:
            self.queue.put(miner)
        return result


    def add(self, miner):
        """
        Enlist a miner in the cause.
        """
        self.all_miners.append(miner)
        return self.queue.put(miner)


    def remove(self, miner):
        """
        Remove a miner from the cause (eventually)
        """
        if miner in self.queue.pending:
            # the miner is idle
            self.all_miners.remove(miner)
            self.queue.pending.remove(miner)
            return miner
        else:
            # the miner is out doing something
            d = defer.Deferred()
            self._to_remove.append((miner, d))
            return d
        


    def listMiners(self):
        """
        List all the miners in the pool (whether busy or not).
        """
        return self.all_miners