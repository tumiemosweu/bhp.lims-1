# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Botswana Harvard Partnership (BHP)

from bhp.lims import api
from bhp.lims import bhpMessageFactory as _
from senaite.core.listing import utils
from senaite.core.listing.interfaces import IListingView
from senaite.core.listing.interfaces import IListingViewAdapter
from zope.component import adapts
from zope.interface import implements


class ClientsListingViewAdapter(object):
    adapts(IListingView)
    implements(IListingViewAdapter)

    # Order of priority of this subscriber adapter over others
    priority_order = 1000

    def __init__(self, listing, context):
        self.listing = listing
        self.context = context

    def before_render(self):
        self.add_columns()

    def folder_item(self, obj, item, index):
        obj = api.get_object(obj)
        commercial_name = api.get_field_value(obj, "CommercialName", "")
        item["getCommercialName"] = commercial_name
        return item

    def add_columns(self):
        bhp_columns = {
            "getCommercialName": {
                "title": _("Commercial Name"),
                "toggle": True,
                "sortable": False,
                "after": "getClientID",
            }
        }

        # Add the columns
        rv_keys = map(lambda r: r["id"], self.listing.review_states)
        for column_id, column_values in bhp_columns.items():
            utils.add_column(listing=self.listing,
                             column_id=column_id,
                             column_values=column_values,
                             after=column_values["after"],
                             review_states=rv_keys)
