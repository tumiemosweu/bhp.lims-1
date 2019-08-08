# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Botswana Harvard Partnership (BHP)

from AccessControl.SecurityInfo import ModuleSecurityInfo
from bhp.lims import api

security = ModuleSecurityInfo(__name__)

@security.public
def guard_make_prospective(client):
    """ Guard for making an object "Prospective"
    """
    commercial_name = api.get_field_value(client, "CommercialName", None)
    if not commercial_name:
        return False
    return True
