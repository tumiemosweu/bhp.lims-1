# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Botswana Harvard Partnership (BHP)

from AccessControl import ClassSecurityInfo

from Products.Archetypes.public import registerType
from bhp.lims.config import PRODUCT_NAME
from bhp.lims.interfaces import IReferralLab
from bika.lims.content.organisation import Organisation
from bika.lims.interfaces import IDeactivable
from zope.interface import implements
from bika.lims.idserver import renameAfterCreation

schema = Organisation.schema.copy()


class ReferralLab(Organisation):
    """A Referral Laboratory the main laboratory requests some analyses to
    """
    implements(IReferralLab, IDeactivable)

    security = ClassSecurityInfo()
    displayContentsTab = False
    schema = schema
    _at_rename_after_creation = True

    def _renameAfterCreation(self, check_auto_id=False):
        renameAfterCreation(self)

registerType(ReferralLab, PRODUCT_NAME)
