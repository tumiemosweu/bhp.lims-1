# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Botswana Harvard Partnership (BHP)

from bhp.lims import api
from bhp.lims.browser.requisition import generate_requisition_pdf
from bhp.lims.interfaces import IDetachedPartition
from bika.lims import workflow as wf
from bika.lims.interfaces import IAnalysisRequestPartition
from bika.lims.workflow.analysisrequest import events
from zope.interface.declarations import noLongerProvides, alsoProvides


def after_no_sampling_workflow(analysis_request):
    """ Event fired for no_sampling_workflow that makes the status of the
    Analysis request or Sample to become sample_ordered
    """
    if not analysis_request.isPartition():
        # Generate the delivery pdf
        generate_requisition_pdf(analysis_request)

    # Set specifications by default
    sample_type = analysis_request.getSampleType()
    specs = api.get_field_value(sample_type, "DefaultAnalysisSpecifications",
                                 None)
    if specs:
        analysis_request.setSpecification(api.get_object(specs))
    else:
        # Find out suitable specs by Sample Type name
        sample_type_title = sample_type.Title()
        specs_title = "{} - calculated".format(sample_type_title)
        query = dict(portal_type="AnalysisSpec", title=specs_title)
        specs = api.search(query, 'bika_setup_catalog')
        if specs:
            analysis_request.setSpecification(api.get_object(specs[0]))

    if analysis_request.isPartition():
        # Change workflow state to "at_reception"
        wf.changeWorkflowState(analysis_request, wf_id="bika_ar_workflow",
                               state_id="sample_at_reception")


def after_deliver(analysis_request):
    """ Event fired after delivery transition is triggered.
    """
    analysis_request.reindexObject(idxs=["getDateReceived", ])


def after_send_to_pot(analysis_request):
    """Event fired after sending to point of testing
    """
    events.do_action_to_ancestors(analysis_request, "send_to_pot")
    events.do_action_to_descendants(analysis_request, "send_to_pot")


def after_receive(analysis_request):
    """Method triggered after "receive" transition for the Analysis Request
    passed in is performed
    """
    events.after_receive(analysis_request)

    # Set the date the Sample was received at the lab, not at point of testing
    # https://github.com/bhp-lims/bhp.lims/issues/233
    date_received = wf.getTransitionDate(analysis_request, "deliver", True)
    if date_received:
        analysis_request.setDateReceived(date_received)

    events.do_action_to_ancestors(analysis_request, "receive")
    events.do_action_to_descendants(analysis_request, "receive")


def after_detach(analysis_request):
    """Method triggered after "detach" transition for the Analysis Request
    passed in is performed
    """
    parent = analysis_request.getParentAnalysisRequest()
    analysis_request.setParentAnalysisRequest(None)
    api.set_field_value(analysis_request, "DetachedFrom", parent)

    # We unmark this analysis request as a Partition
    noLongerProvides(analysis_request, IAnalysisRequestPartition)

    # And we add the marker IDetachedPartition
    alsoProvides(analysis_request, IDetachedPartition)

    # Reindex both the parent and the one we've detached
    analysis_request.reindexObject()
    parent.reindexObject()
