# -*- coding: utf-8 -*-

from bika.lims import api
from bika.lims.interfaces import IReceived
from bika.lims.utils import changeWorkflowState
from bika.lims.utils.analysisrequest import fields_to_dict, \
    create_analysisrequest
from bika.lims.workflow import ActionHandlerPool
from bika.lims.workflow import doActionFor
from zope.interface import alsoProvides


def create_partition(analysis_request, request, analyses, sample_type=None,
                     container=None, preservation=None, skip_fields=None,
                     remove_primary_analyses=True, internal_use=True):
    """
    Creates a partition for the analysis_request (primary) passed in
    :param analysis_request: uid/brain/object of IAnalysisRequest type
    :param request: the current request object
    :param analyses: uids/brains/objects of IAnalysis type
    :param sampletype: uid/brain/object of SampleType
    :param container: uid/brain/object of Container
    :param preservation: uid/brain/object of Preservation
    :param skip_fields: names of fields to be skipped on copy from primary
    :param remove_primary_analyses: removes the analyses from the parent
    :return: the new partition
    """
    partition_skip_fields = [
        "Analyses",
        "Attachment",
        "Client",
        "DetachedFrom",
        "Profile",
        "Profiles",
        "RejectionReasons",
        "Remarks",
        "ResultsInterpretation",
        "ResultsInterpretationDepts",
        "Sample",
        "Template",
        "creation_date",
        "id",
        "modification_date",
        "ParentAnalysisRequest",
        "PrimaryAnalysisRequest",
    ]
    if skip_fields:
        partition_skip_fields.extend(skip_fields)
        partition_skip_fields = list(set(partition_skip_fields))

    # Copy field values from the primary analysis request
    ar = api.get_object(analysis_request)
    record = fields_to_dict(ar, partition_skip_fields)

    # Update with values that are partition-specific
    record.update({
        "InternalUse": internal_use,
        "ParentAnalysisRequest": api.get_uid(ar),
    })
    if sample_type is not None:
        record["SampleType"] = sample_type and api.get_uid(sample_type) or ""
    if container is not None:
        record["Container"] = container and api.get_uid(container) or ""
    if preservation is not None:
        record["Preservation"] = preservation and api.get_uid(preservation) or ""

    # Create the Partition
    client = ar.getClient()
    analyses = list(set(map(api.get_object, analyses)))
    services = map(lambda an: an.getAnalysisService(), analyses)
    specs = ar.getSpecification()
    specs = specs and specs.getResultsRange() or []
    partition = create_analysisrequest(client, request=request, values=record,
                                       analyses=services, specifications=specs)

    # Remove analyses from the primary
    if remove_primary_analyses:
        analyses_ids = map(api.get_id, analyses)
        ar.manage_delObjects(analyses_ids)

    # Reindex Parent Analysis Request
    ar.reindexObject(idxs=["isRootAncestor"])

    # Manually set the Date Received to match with its parent. This is
    # necessary because crar calls to processForm, so DateReceived is not
    # set because the partition has not been received yet
    partition.setDateReceived(ar.getDateReceived())
    partition.reindexObject(idxs="getDateReceived")

    # Force partition to same status as the primary
    status = api.get_workflow_status_of(ar)
    changeWorkflowState(partition, "bika_ar_workflow", status)
    if IReceived.providedBy(ar):
        alsoProvides(partition, IReceived)

    # And initialize the analyses the partition contains. This is required
    # here because the transition "initialize" of analyses rely on a guard,
    # so the initialization can only be performed when the sample has been
    # received (DateReceived is set)
    ActionHandlerPool.get_instance().queue_pool()
    for analysis in partition.getAnalyses(full_objects=True):
        doActionFor(analysis, "initialize")
    ActionHandlerPool.get_instance().resume()
    return partition
