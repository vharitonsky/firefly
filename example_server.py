import time
from wsgiref.simple_server import make_server
from caching_middleware import cache_middleware

def simple_app(environ, start_response):
    time.sleep(3)# perform heavy computation
    start_response('200 OK', [('Content-type', 'text/plain')])
    return  ["Hello world"]

if __name__ == '__main__':
    make_server('', 8000, cache_middleware(simple_app, 'memc:127.0.0.1:11211')).serve_forever()
