from Products.Five.browser import BrowserView


class MyFirstView(BrowserView):

    def __init__(self, context, request):
        super(MyFirstView, self).__init__(context, request)
        self.context = context
        self.request = request

    def __call__(self, *args, **kwargs):
        return "Say hi"
