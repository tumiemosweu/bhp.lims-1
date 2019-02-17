# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Botswana Harvard Partnership (BHP)

from bhp.lims.workflow.analysisrequest import events


def AfterTransitionEventHandler(analysis_request, event):
    """Actions to be done when a transition for an analysis request takes place
    """
    if not event.transition:
        return

    function_name = "after_{}".format(event.transition.id)
    if hasattr(events, function_name):
        # Call the after_* function from events package
        getattr(events, function_name)(analysis_request)
