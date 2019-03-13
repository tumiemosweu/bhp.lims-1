# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Botswana Harvard Partnership (BHP)


from bika.lims.adapters.widgetvisibility import SenaiteATWidgetVisibility
from bika.lims import api


class AssayDateVisibility(SenaiteATWidgetVisibility):
    """
    Handles "AssayDate" field visibility. Field can only be edited when the
    status of the Analysis Request is in `to_be_verified` and the current user
    has the role "LabManager" for the current context
    """
    def __init__(self, context):
        super(AssayDateVisibility, self).__init__(
            context=context, sort=10,
            field_names=["AssayDate", ])

    def isVisible(self, field, mode="view", default="visible"):
        edit_modes = ["sample_received", "to_be_verified"]
        if mode == "edit":
            if api.get_review_status(self.context) not in edit_modes:
                return "invisible"

            # Only Lab Manager can edit Assay Date!
            allowed_roles = ["LabManager", "Manager", "Analyst"]
            user = api.get_current_user()
            user_roles = user.getRolesInContext(self.context)
            allowed_roles = filter(lambda r: r in user_roles, allowed_roles)
            if not allowed_roles:
                return "invisible"

        return default
