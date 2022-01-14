import hashlib
import json
import pickle

from redis.client import Redis
from functools import wraps, lru_cache


def get_lru_cache_method():
    def cache_with_lru(func):
        return lru_cache(maxsize=1024)(func)
    return cache_with_lru


class HashedSeq(list):
    __slots__ = 'hashvalue'

    def __init__(self, tup, hash=hash):
        self[:] = tup
        self.hashvalue = hash(tup)

    def __hash__(self):
        return self.hashvalue


def make_key(args, kwds, typed,
             kwd_mark=(object(),),
             fasttypes={int, str},
             tuple=tuple, type=type, len=len):
    key = args
    if kwds:
        key += kwd_mark
        for item in kwds.items():
            key += item
    if typed:
        key += tuple(type(v) for v in args)
        if kwds:
            key += tuple(type(v) for v in kwds.values())
    elif len(key) == 1 and type(key[0]) in fasttypes:
        return key[0]
    return HashedSeq(key)


def get_redis_cache_method():
    redis = Redis()

    def cache_with_redis(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            redis_args = (func.__qualname__,) + args
            key = str(make_key(redis_args, kwargs, False))
            key = hashlib.md5(key.encode()).digest()

            result = redis.get(key)

            if result is None:
                value = func(*args, **kwargs)
                value_json = pickle.dumps(value)
                redis.set(key, value_json)
            else:
                # Skip the function entirely and use the cached value instead.
                # value_json = result.decode('utf-8')
                value = pickle.loads(result)

            return value

        return wrapper

    return cache_with_redis
