# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Botswana Harvard Partnership (BHP)

from collections import OrderedDict
from bika.lims import bikaMessageFactory as _
from bika.lims.browser.bika_listing import BikaListingView
from bika.lims.utils import get_link, get_email_link
from bhp.lims.interfaces import ICouriers
from zope.interface import implements


class ClientCouriersView(BikaListingView):
    """Listing view for all Client Couriers
    """
    implements(ICouriers)

    def __init__(self, context, request):
        super(ClientCouriersView, self).__init__(context, request)

        self.catalog = "portal_catalog"



        self.contentFilter = {
            "portal_type": "ClientCourier",
            "sort_on": "sortable_title",
            "sort_order": "ascending",
            'path': {
                "query": "/".join(context.getPhysicalPath()),
                "level": 0
            }
        }

        self.context_actions = {
            _('Add'):
                {'url': 'createObject?type_name=ClientCourier',
                 'permission': 'Add portal content',
                 'icon': '++resource++bika.lims.images/add.png'}}

        self.title = self.context.translate(_("Couriers"))
        self.description = ""
        self.icon = "{}/{}".format(
            self.portal_url,
            "++resource++bhp.images/courier_big.png")

        self.show_select_row = False
        self.show_select_column = True
        self.pagesize = 50
        self.form_id = "clientcouriers"

        self.columns = OrderedDict((
            ("getFullname", {
                "title": _("Full Name"),
                "index": "getFullname",
                "sortable": True, }),
            ("getEmailAddress", {
                "title": _("Email Address"), }),
            ("getBusinessPhone", {
                "title": _("Business Phone"), }),
        ))

        self.review_states = [
            {
                "id": "default",
                "title": _("Active"),
                "contentFilter": {"review_state": "active"},
                "transitions": [{"id": "deactivate"}, ],
                "columns":  self.columns.keys(),
            }, {
                "id": "inactive",
                "title": _("Dormant"),
                "contentFilter": {"review_state": "inactive"},
                "transitions": [{"id": "activate"}, ],
                "columns":  self.columns.keys(),
            }, {
                "id": "all",
                "title": _("All"),
                "contentFilter": {},
                "columns":  self.columns.keys(),
            },
        ]

    def folderitem(self, obj, item, index):
        """Service triggered each time an item is iterated in folderitems.
        The use of this service prevents the extra-loops in child objects.
        :obj: the instance of the class to be foldered
        :item: dict containing the properties of the object to be used by
            the template
        :index: current index of the item
        """

        fullname = obj.getFullname()
        email = obj.getEmailAddress()
        url = item.get("url")
        item['getFullname'] = fullname
        item['getEmailAddress'] = email
        item['getBusinessPhone'] = obj.getBusinessPhone()
        item["replace"]["getFullname"] = get_link(url, fullname)
        if email:
            item["replace"]['getEmailAddress'] = get_email_link(email)

        return item
