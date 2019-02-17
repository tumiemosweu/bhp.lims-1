# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Botswana Harvard Partnership (BHP)

from DateTime import DateTime
from Products.ATContentTypes.utils import DT2dt
from bhp.lims import api
from bika.lims.alphanumber import Alphanumber
from bika.lims.idserver import get_current_year, get_type_id


def get_variables(context, **kw):
    """Prepares a dictionary of key->value pairs usable for ID formatting
    """
    # allow portal_type override
    portal_type = get_type_id(context, **kw)

    # The variables map hold the values that might get into the constructed id
    variables = {
        'context': context,
        'id': api.get_id(context),
        'portal_type': portal_type,
        'year': get_current_year(),
        'parent': api.get_parent(context),
        'seq': 0,
        'alpha': Alphanumber(0),
    }

    # Augment the variables map depending on the portal type
    if portal_type in ["AnalysisRequest", "AnalysisRequestPartition"]:
        now = DateTime()
        sampling_date = context.getSamplingDate()
        sampling_date = sampling_date and DT2dt(sampling_date) or DT2dt(now)
        date_sampled = context.getDateSampled()
        date_sampled = date_sampled and DT2dt(date_sampled) or DT2dt(now)
        variables.update({
            'clientId': context.getClientID(),
            'dateSampled': date_sampled,
            'samplingDate': sampling_date,
            'sampleType': context.getSampleType().getPrefix(),
            'studyId': context.aq_parent.getTaxNumber(),
        })
        if portal_type == "AnalysisRequestPartition":
            parent_ar = context.getParentAnalysisRequest()
            variables.update({
                "parent_analysisrequest": parent_ar,
                "parent_ar_id": api.get_id(parent_ar)
            })

    elif portal_type == "ARReport":
        variables.update({
            'clientId': context.aq_parent.getClientID(),
        })

    return variables
