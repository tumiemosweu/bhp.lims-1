# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Botswana Harvard Partnership (BHP)

import logging

from AccessControl import allow_module
from Products.Archetypes.atapi import listTypes
from Products.Archetypes.atapi import process_types
from Products.CMFCore.permissions import AddPortalContent
from Products.CMFCore.utils import ContentInit
from zope.i18nmessageid import MessageFactory

from config import PRODUCT_NAME

# Make bhp.* modules importable by through-the-web
# https://docs.plone.org/develop/plone/security/sandboxing.html
# https://docs.zope.org/zope2/zdgbook/Security.html
# This allows Script python (e.g. guards from skins) to access to these modules.
# To provide access to a module inside of a package, we need to provide security
# declarations for all of the the packages and sub-packages along the path
# used to access the module. Thus, all the modules from the path passed in to
# `allow_module` will be available.
allow_module('bhp.lims.workflow.analysisrequest.guards')

# Defining a Message Factory for when this product is internationalized.
bhpMessageFactory = MessageFactory('bhp')
logger = logging.getLogger(PRODUCT_NAME)


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    logger.info("*** Initializing BHP LIMS Customization Package ***")

    from content.courier import Courier # noqa
    from content.couriers import Couriers # noqa

    from content.clientcourier import ClientCourier

    from bhp.lims.content.barcodeprinter import BarcodePrinter  # noqa
    from bhp.lims.controlpanel.barcodeprinters import BarcodePrinters # noqa

    from bhp.lims.content.referrallab import ReferralLab  # noqa
    from bhp.lims.content.referrallabs import ReferralLabs # noqa

    types = listTypes(PRODUCT_NAME)
    content_types, constructors, ftis = process_types(types, PRODUCT_NAME)

    # Register each type with it's own Add permission
    # use ADD_CONTENT_PERMISSION as default
    allTypes = zip(content_types, constructors)
    for atype, constructor in allTypes:
        kind = "%s: Add %s" % (PRODUCT_NAME, atype.portal_type)
        ContentInit(kind,
                    content_types=(atype,),
                    permission=AddPortalContent,
                    extra_constructors=(constructor, ),
                    fti=ftis,
                    ).initialize(context)
