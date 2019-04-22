# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Botswana Harvard Partnership (BHP)

from bhp.lims.workflow.analysis import events


def AfterTransitionEventHandler(analysis, event):
    """Actions to be done when a transition for an analysis takes place
    """
    if not event.transition:
        return

    function_name = "after_{}".format(event.transition.id)
    if hasattr(events, function_name):
        # Call the after_* function from events package
        getattr(events, function_name)(analysis)


def BeforeTransitionEventHandler(analysis, event):
    """Actions to be done before a transition for an analysis takes place
    """
    if not event.transition:
        return

    function_name = "before_{}".format(event.transition.id)
    if hasattr(events, function_name):
        # Call the after_* function from events package
        getattr(events, function_name)(analysis)
