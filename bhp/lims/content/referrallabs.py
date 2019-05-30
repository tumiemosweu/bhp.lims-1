# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Botswana Harvard Partnership (BHP)

from Products.ATContentTypes.content import schemata
from Products.Archetypes import atapi
from bhp.lims.config import PRODUCT_NAME
from bhp.lims.interfaces import IReferralLabs
from plone.app.folder.folder import ATFolder
from plone.app.folder.folder import ATFolderSchema
from zope.interface.declarations import implements

schema = ATFolderSchema.copy()


class ReferralLabs(ATFolder):
    implements(IReferralLabs)
    displayContentsTab = False
    schema = schema


schemata.finalizeATCTSchema(schema, folderish=True, moveDiscussion=False)
atapi.registerType(ReferralLabs, PRODUCT_NAME)
