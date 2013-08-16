# sync.py
from itertools import product
from toyminer.validate import validAnswer



class SyncMiner(object):

    pool = map(chr, xrange(0, 255))


    def _options(self, pool):
        """
        Return gradually lengthening selections of pool.

        For instance, if pool is ABCD, return

            A, B, C, D, AA, AB, AC, AD, BA, BB, BC, BD
        """
        i = 1
        while True:
            for p in product(pool, repeat=i):
                yield ''.join(p)
            i += 1


    def mine(self, given_hash, difficulty, scale):
        for o in self._options(self.pool):
            if validAnswer(given_hash, difficulty, scale, o):
                return o
        return ''
