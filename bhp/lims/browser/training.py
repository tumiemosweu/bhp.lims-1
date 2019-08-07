from Products.Five.browser import BrowserView
from bika.lims import api


class MyFirstView(BrowserView):

    def __init__(self, context, request):
        super(MyFirstView, self).__init__(context, request)
        self.context = context
        self.request = request

    def __call__(self, *args, **kwargs):

        query = dict(
            portal_type="Client",
            is_active=True,)

        results = api.search(query, "portal_catalog")
        titles = map(api.get_title, results)
        return ", ".join(titles)
