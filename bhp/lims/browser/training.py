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
            is_active=True,)

        brains = api.search(query, "portal_catalog")
        for brain in brains:
            client_id_from_brain = brain.getClientID
            client_id_from_object = api.get_object(brain).getClientID()
            logger.info("{} == {}".format(client_id_from_brain, client_id_from_object))

        titles = map(api.get_title, brains)
        return ", ".join(titles)
