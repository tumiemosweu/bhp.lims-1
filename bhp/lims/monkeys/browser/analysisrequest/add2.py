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
