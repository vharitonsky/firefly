from wsgiref.simple_server import make_server
from caching_middleware import cache_middleware

def simple_app(environ, start_response):
    start_response('200 OK', [('Content-type', 'text/plain')])
    return  ["Hello world"]

if __name__ == '__main__':
    make_server('', 8000, cache_middleware(simple_app, 'file:data')).serve_forever()
