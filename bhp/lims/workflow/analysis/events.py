# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Botswana Harvard Partnership (BHP)

from bhp.lims.api import set_field_value
from bhp.lims import api
from bika.lims.interfaces.analysis import IRequestAnalysis


def after_submit(analysis):
    """Actions to be done after a submit transition for an analysis takes place
    """
    analysis = api.get_object(analysis)
    if IRequestAnalysis.providedBy(analysis):
        ar = analysis.getRequest()
        set_field_value(ar, "AssayDate", analysis.getDateSubmitted())
