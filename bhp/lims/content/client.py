# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Botswana Harvard Partnership (BHP)
from Products.Archetypes.Widget import StringWidget
from Products.CMFCore.permissions import View, ModifyPortalContent
from archetypes.schemaextender.interfaces import ISchemaModifier, \
    IOrderableSchemaExtender
from bika.lims import bikaMessageFactory as _
from bika.lims.fields import ExtStringField
from bika.lims.interfaces import IClient
from zope.component import adapts
from zope.interface import implements

fields = [
    ExtStringField(
        "CommercialName",
        mode="rw",
        required=0,
        read_permission=View,
        write_permission=ModifyPortalContent,
        widget=StringWidget(
            label=_("Commercial Name")
        )
    )
]

class ClientSchemaExtender(object):
    adapts(IClient)
    implements(IOrderableSchemaExtender)

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        return schematas

    def getFields(self):
        return fields


class ClientSchemaModifier(object):
    adapts(IClient)
    implements(ISchemaModifier)

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        schema['TaxNumber'].widget.label = _("Study Code")
        return schema
