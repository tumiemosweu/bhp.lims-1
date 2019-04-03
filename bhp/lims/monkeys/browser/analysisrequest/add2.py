# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Botswana Harvard Partnership (BHP)

from bhp.lims import api
from bhp.lims import setuphandlers as handler


def flush(self):
    """Restore the sorting and visibility of fields from AR Add form
    """
    portal = api.get_portal()
    handler.sort_ar_add_fields(portal)
    handler.hide_ar_add_fields(portal)


def get_records(self):
    """Returns a list of AR records

    Fields coming from `request.form` have a number prefix, e.g. Contact-0.
    Fields with the same suffix number are grouped together in a record.
    Each record represents the data for one column in the AR Add form and
    contains a mapping of the fieldName (w/o prefix) -> value.

    Example:
    [{"Contact": "Rita Mohale", ...}, {Contact: "Neil Standard"} ...]
    """
    form = self.request.form
    ar_count = self.get_ar_count()

    records = []
    # Group belonging AR fields together
    for arnum in range(ar_count):
        record = {}
        s1 = "-{}".format(arnum)
        keys = filter(lambda key: s1 in key, form.keys())
        for key in keys:
            new_key = key.replace(s1, "")
            # Handle BHP-specific Volume field
            if new_key == "Volume":
                vol = form.get("{}_volume".format(key), "")
                if vol:
                    unit = form.get("{}_unit".format(key), "")
                    value = "{} {}".format(vol, unit)
                    record[new_key] = value
            else:
                value = form.get(key)
                record[new_key] = value
        records.append(record)
    return records