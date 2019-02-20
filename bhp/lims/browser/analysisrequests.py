# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Botswana Harvard Partnership (BHP)
# -*- coding: utf-8 -*-

from bhp.lims import api
from bhp.lims import bhpMessageFactory as _
from senaite.core.listing import utils
from senaite.core.listing.interfaces import IListingView
from senaite.core.listing.interfaces import IListingViewAdapter
from zope.component import adapts
from zope.interface import implements


class AnalysisRequestsListingViewAdapter(object):
    adapts(IListingView)
    implements(IListingViewAdapter)

    def __init__(self, listing, context):
        self.listing = listing
        self.context = context

    def get_priority_order(self):
        """Returns a number that represents the order of priority of this
        subscriber adapter over other subscriber adapters for same context
        and listing view
        """
        return 9999

    def before_render(self):
        # Additional columns
        self.add_columns()
        # Additional filter buttons (review_states)
        self.add_review_states()
        # Additional custom actions
        self.add_custom_transitions()

    def folder_item(self, obj, item, index):
        return item

    def add_columns(self):
        """Adds bhp-specific olumns in the listing
        """
        bhp_columns = {
            # Participant ID
            "getParticipantID": {
                "title": _("Participant ID"),
                "index": "getParticipantID",
                "sortable": True,
                "toggle": True,
                "after": "getClientSampleID"
            },
            # Visit Number
            "getVisit": {
                "title": _("Visit Code"),
                "attr": "getVisit",
                "sortable": False,
                "toggle": True,
                "after": "getParticipantID"
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

    def add_review_states(self):
        """Adds bhp-specific review states (filter buttons) in the listing
        """
        # Get the columns and custom actions set by default for sample_due
        sample_due = filter(lambda o: o["id"] == "sample_due",
                            self.listing.review_states)[0]
        default_columns = sample_due["columns"]
        default_actions = sample_due.get("custom_transitions", [])

        bhp_review_states = [
            # Sample ordered
            {"id": "sample_ordered",
             "title": _("Ordered"),
             "contentFilter": {
                 "review_state": ("sample_ordered",),
                 "sort_on": "created",
                 "sort_order": "descending"},
             "transitions": [],
             "custom_transitions": default_actions,
             "columns": default_columns, },

            # Sample shipped
            {"id": "sample_shipped",
             "title": _("Shipped"),
             "contentFilter": {
                 "review_state": ("sample_shipped",),
                 "sort_on": "created",
                 "sort_order": "descending"},
             "transitions": [],
             "custom_transitions": default_actions,
             "columns": default_columns, },

            # Sample at reception
            {"id": "sample_at_reception",
             "title": _("At reception"),
             "contentFilter": {
                 "review_state": ("sample_at_reception",),
                 "sort_on": "created",
                 "sort_order": "descending"},
             "transitions": [],
             "custom_transitions": default_actions,
             "columns": default_columns,}
        ]

        # Add the review states
        for bhp_review_state in bhp_review_states:
            utils.add_review_state(listing=self.listing,
                                   review_state=bhp_review_state,
                                   before="sample_due")

        # Add bhp custom states to "active" filter
        bhp_state_ids = map(lambda r: r["id"], bhp_review_states)
        for rv_filter in self.listing.review_states:
            if rv_filter["id"] == "default":
                review_states = rv_filter["contentFilter"]["review_state"]
                review_states = list(review_states) + bhp_state_ids
                review_states = tuple(set(review_states))
                rv_filter["contentFilter"]["review_state"] = review_states
                break

    def add_custom_transitions(self):
        """Adds custom transitions to review_states
        """
        # States where we want the custom transition
        document_ico = api.get_html_image("document.png")
        custom_transitions = [
            {"id": "download_requisition",
             "title": "{} Requisition".format(document_ico),
             "url": "workflow_action?action=download_requisition",
             "review_states": [
                 "default",
                 "sample_ordered",
                 "sample_shipped",
                 "sample_at_reception"
             ],
             "after": "print_stickers"},

            # TODO Uncomment once we assign only 1 Delivery Attachment per AR
            # At that point, we'll be able to only delivery the non-overlaping
            # pdfs for a set of selected ARs.
            #
            # {"id": "download_delivery",
            # "title": "{} Delivery".format(document_ico),
            # "url": "workflow_action?action=download_delivery",
            # "review_states": [
            #     "sample_shipped",
            #     "sample_at_reception"
            # ],
            # "after": "print_stickers"},

        ]

        # Add the custom transitions to review_states
        for custom in custom_transitions:
            rev_state_ids = custom.get("review_states", None)
            self.add_custom_transition(custom, review_state_ids=rev_state_ids)


    def add_custom_transition(self, transition, review_state_ids=None):
        """Adds a custom transition to the review state ids passed in. If
        review states are not specified, adds the transition to all. Returns
        a list with the updated review_states
        """
        added = []
        action_id = transition["id"]
        for review_state in self.listing.review_states:
            if review_state_ids and review_state["id"] not in review_state_ids:
                continue

            # No need to add the transition again if already exists
            old_custom = review_state.get("custom_transitions", [])
            old_custom_ids = map(lambda o: o.get("id", ""), old_custom)
            if action_id in old_custom_ids:
                continue

            # Add the transition
            idx=0
            after = transition.get("after", None)
            before = transition.get("before", None)
            if after and after in old_custom_ids:
                idx = old_custom_ids.index(after) + 1
            elif before and before in old_custom_ids:
                idx = old_custom_ids.index(before)
            old_custom.insert(idx, transition)
            added.append(review_state["id"])

        return added
