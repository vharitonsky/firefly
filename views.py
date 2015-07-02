from util import controller, Response, Router

@controller
def index(request):
    return Response(200, "It works!")

@controller
def hello(request):
    return Response(200, "Hello %s" % request.GET.get('name', "Anonymous"))

router = Router({
    '/index': index,
    '/hello': hello,
})
