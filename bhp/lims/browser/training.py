from StringIO import StringIO

from DateTime import DateTime
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from bhp.lims import logger
from bhp.lims import api


class MyFirstView(BrowserView):
    template = ViewPageTemplateFile("templates/my_first_view.pt")

    def __init__(self, context, request):
        super(MyFirstView, self).__init__(context, request)
        self.context = context
        self.request = request
        self._clients = None
        self.request.set("disable_border", 1)

    @property
    def clients(self):
        if not self._clients:
            self._clients = self.search()
        return self._clients

    def __call__(self, *args, **kwargs):
        logger.info("Rendering MyFirstView ...")
        form = self.request.form

        # Form submit toggle
        form_submitted = form.get("submitted", False)

        # Buttons
        form_to_csv = form.get("button_to_csv", False)

        # Handle export to csv
        if form_submitted and form_to_csv:
            logger.info("*** Exporting to CSV ***")
            return self.get_csv()

        return self.template()

    def search(self):
        query = dict(
            portal_type="Client",
            sort_on="sortable_title",
            sort_order="ascending",
            is_active=True,)

        brains = api.search(query, "portal_catalog")
        return map(api.get_object, brains)

    def get_csv(self):
        output = StringIO()
        lines = []
        for client in self.clients:
            client_title = client.Title()
            client_id = client.getClientID()
            client_commercial = api.get_field_value(client, "CommercialName", "")
            lines.append([client_title, client_commercial, client_id])

        header = ["Title", "Commercial Name", "Client ID"]
        lines.insert(0, header)
        for line in lines:
            output.write(",".join(line) + "\n")
        return output.getvalue()
