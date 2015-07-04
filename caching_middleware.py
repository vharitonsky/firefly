import os
import hashlib
from collections import namedtuple

CacheBackend = namedtuple("CacheBackend", ["get", "set", "exists"])


def inprocess_backend():
    cache = {}

    def get(key):
        return cache.get(key)

    def set(key, value):
        cache[key] = value

    def exists(key):
        return key in cache

    return CacheBackend(get, set, exists)

def file_backend(dir_path):
    import cPickle
    
    def _path(key):
        return os.path.join(dir_path, key)

    def get(key):
        path = _path(key)
        if not os.path.exists(path):
            return None
        with open(path) as f:
            return cPickle.load(f)

    def set(key, value):
        with open(_path(key), 'w') as f:
            cPickle.dump(value, f)

    def exists(key):
        return os.path.exists(_path(key))

    return CacheBackend(get, set, exists)


def memcached_backend(addr):
    import memcache
    mc = memcache.Client([addr])

    def get(key):
        return mc.get(key)

    def set(key, value):
        return mc.set(key, value)

    def exists(key):
        return mc.get(key) is not None

    return CacheBackend(get, set, exists)


def get_backend(backend):
    if backend is None:
        return inprocess_backend()
    name, config = backend.split(':')
    return {
        'file': file_backend,
        'memcached': memcached_backend
    }[name](config)


def get_cache_key(environ):
    raw_key = unicode((environ['PATH_INFO'], environ['QUERY_STRING']))
    return hashlib.sha1(raw_key).hexdigest()


def cache_middleware(app, backend=None):
  
    cache = get_backend(backend)
      
    def caching_app(environ, start_response):
        mutable_headers = []
        key = get_cache_key(environ)

        def caching_start_response(status, headers):
            mutable_headers.append((status, headers))
            start_response(status, headers)

        if cache.exists(key):
            (status, headers), body = cache.get(key)
            start_response(status, headers)
            return body
        else:
            result = app(environ, caching_start_response)
            cache.set(key, (mutable_headers[0], result))
            return result

    return caching_app

        
