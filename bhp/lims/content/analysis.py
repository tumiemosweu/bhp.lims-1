# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Botswana Harvard Partnership (BHP)

from Products.CMFCore.permissions import View
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaExtender
from bhp.lims.content import ExtUIDReferenceField
from bhp.lims.interfaces import IBhpLIMS
from bika.lims.interfaces import IAnalysis
from zope.component import adapts
from zope.interface import implements


class AnalysisSchemaExtender(object):
    """Extend Analysis with additional schema fields
    """
    adapts(IAnalysis)

    implements(
        ISchemaExtender,
        IBrowserLayerAwareExtender)

    # Don't do schema extending unless our add-on product is
    # installed on Plone site
    layer = IBhpLIMS

    # Referral Lab where this test is performed
    fields = [
        ExtUIDReferenceField(
            "ReferralLab",
            mode="rw",
            required=0,
            multiValued=0,
            read_permission=View,
            write_permission="Field: Edit Result",
            allowed_types=('ReferralLab',),
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields
