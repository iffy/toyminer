# toyminer/solver.py
from itertools import product
from toyminer.validate import validAnswer

POOL = map(chr, xrange(0, 255))

def _options(pool):
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


def mine(given_hash, difficulty, scale):
    """
    Brute force a string that will satisfy the problem for the given args.
    """
    for o in _options(POOL):
        if validAnswer(given_hash, difficulty, scale, o):
            return o
    return ''
