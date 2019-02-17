# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Botswana Harvard Partnership (BHP)

from bhp.lims import api
from bika.lims.interfaces import IAnalysisRequest
from plone.indexer import indexer


@indexer(IAnalysisRequest)
def getParticipantID(instance):
    """Returns the patient ID of the current Analysis Request
    """
    return api.get_field_value(instance, "ParticipantID", default="")

@indexer(IAnalysisRequest)
def getVisit(instance):
    """Returns the visit number of the current Analysis Request
    """
    return api.get_field_value(instance, "Visit", default="")
