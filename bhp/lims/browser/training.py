from Products.Five.browser import BrowserView
from bhp.lims import logger
from bika.lims import api


class MyFirstView(BrowserView):

    def __init__(self, context, request):
        super(MyFirstView, self).__init__(context, request)
        self.context = context
        self.request = request

    def __call__(self, *args, **kwargs):

        query = dict(
            portal_type="Client",
            sort_on="sortable_title",
            sort_order="ascending",
            is_active=True,)

        brains = api.search(query, "portal_catalog")
        titles = map(api.get_title, brains)
        return ", ".join(titles) or "No results"
