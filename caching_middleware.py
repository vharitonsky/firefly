import hashlib
from cache_backends import get_backend

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

        
