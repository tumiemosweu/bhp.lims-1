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


class AnalysesListingViewAdapter(object):
    adapts(IListingView)
    implements(IListingViewAdapter)

    def __init__(self, listing, context):
        self.listing = listing
        self.context = context

    def before_render(self):
        # Additional columns
        self.add_columns()

    def add_columns(self):
        """Adds bhp-specific columns in the listing
        """
        bhp_columns = {
            # Referral Laboratory
            "ReferralLab": {
                "title": _("Referral Lab"),
                "index": "getReferralLabUID",
                "sortable": False,
                "toggle": True,
                "ajax": True,
                "after": "retested"
            },
        }

        # Add the columns
        rv_keys = map(lambda r: r["id"], self.listing.review_states)
        for column_id, column_values in bhp_columns.items():
            utils.add_column(listing=self.listing,
                             column_id=column_id,
                             column_values=column_values,
                             after=column_values["after"],
                             review_states=rv_keys)

    def folder_item(self, obj, item, index):
        # Folder "ReferralLab" item
        self.folder_referral_lab(obj, item, index)
        return item

    def folder_referral_lab(self, obj, item, index):
        """Adds the column Referral Lab to the item
        """
        is_editable = self.listing.is_analysis_edition_allowed(obj)
        obj = api.get_object(obj)
        ref_lab = api.get_field_value(obj, "ReferralLab", None)
        if not is_editable:
            ref_lab_title = ref_lab and api.get_title(ref_lab) or ""
            item["ReferralLab"] = ref_lab_title
            return item

        # Referral Laboratory is editable
        item["ReferralLab"] = ref_lab and api.get_uid(ref_lab) or ""
        item["choices"]["ReferralLab"] = self.get_referral_labs()
        item['allow_edit'].append('ReferralLab')
        return item

    def get_referral_labs(self):
        """Returns a list for selection with the available and active
        Referral Lab objects, sorted by title ascending
        """
        empty = {"ResultValue": "", "ResultText": ""}
        results = list([empty,])
        query = dict(portal_type="ReferralLab", is_active=True,
                     sort_on="sortable_title")
        for brain in api.search(query, "bika_setup_catalog"):
            results.append({"ResultValue": api.get_uid(brain),
                            "ResultText": api.get_title(brain)})
        return results
