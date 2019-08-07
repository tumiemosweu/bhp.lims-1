from Products.Five.browser import BrowserView
from bhp.lims import logger
from bika.lims import api
from z3c.pt.pagetemplate import ViewPageTemplateFile


class MyFirstView(BrowserView):
    template = ViewPageTemplateFile("templates/my_first_view.pt")

    def __init__(self, context, request):
        super(MyFirstView, self).__init__(context, request)
        self.context = context
        self.request = request
        self._clients = None

    @property
    def clients(self):
        if not self._clients:
            self._clients = self.search()
        return self._clients

    def __call__(self, *args, **kwargs):
        return self.template()

    def search(self):
        query = dict(
            portal_type="Client",
            sort_on="sortable_title",
            sort_order="ascending",
            is_active=True,)

        brains = api.search(query, "portal_catalog")
        return map(api.get_object, brains)
