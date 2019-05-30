# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Botswana Harvard Partnership (BHP)

from archetypes.schemaextender.field import ExtensionField
from bika.lims.browser.fields import UIDReferenceField


class ExtUIDReferenceField(ExtensionField, UIDReferenceField):
    """Holds an UID reference to an object
    """
