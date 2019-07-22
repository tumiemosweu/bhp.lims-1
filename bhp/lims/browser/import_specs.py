# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Botswana Harvard Partnership (BHP)

from Products.Five.browser import BrowserView
from bhp.lims import api
from bhp.lims.setuphandlers import import_specifications


class ImportSpecificationsView(BrowserView):
    """Import the specifications from the xlsx file
    """

    def __init__(self, context, request):
        super(ImportSpecificationsView, self).__init__(context, request)
        self.context = context
        self.request = request

    def __call__(self):
        import_specifications(api.get_portal())
        return "Specifications imported"