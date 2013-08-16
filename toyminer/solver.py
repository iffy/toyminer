from hashlib import sha1
from itertools import product

MAX_SHA = int('f'*40, 16)


def options(pool):
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


def validAnswer(given_hash, difficulty, scale, answer):
    result = int(sha1(given_hash + answer).hexdigest(), 16)
    threshold = (scale - difficulty) * (MAX_SHA / scale)
    return result > threshold



class SyncMiner(object):

    pool = map(chr, xrange(0, 255))

    def mine(self, given_hash, difficulty, scale):
        for o in options(self.pool):
            if validAnswer(given_hash, difficulty, scale, o):
                return o
        return ''



def main(given_hash, difficulty, scale):
    return SyncMiner().mine(given_hash, difficulty, scale)


if __name__ == '__main__':
    import sys
    given_hash = sys.argv[1]
    difficulty, scale = map(int, sys.argv[2:])
    sys.stdout.write(main(given_hash, difficulty, scale))