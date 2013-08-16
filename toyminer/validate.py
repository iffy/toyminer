# validate.py
from hashlib import sha1

MAX_SHA = int('f'*40, 16)



def validAnswer(given_hash, difficulty, scale, answer):
    result = int(sha1(given_hash + answer).hexdigest(), 16)
    threshold = (scale - difficulty) * (MAX_SHA / scale)
    return result > threshold
