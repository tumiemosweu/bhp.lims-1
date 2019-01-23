from bhp.lims.api import get_field_value
from bika.lims import api
from bika.lims.interfaces import IAnalysisRequest
from bika.lims.interfaces.analysis import IRequestAnalysis
from plone.indexer import indexer


@indexer(IRequestAnalysis)
def getAncestorsUIDs(instance):
    """Returns the UIDs of all the ancestors (Analysis Requests) this analysis
    comes from
    """
    request = instance.getRequest()
    parents = map(lambda ar: api.get_uid(ar), request.getAncestors())
    return [api.get_uid(request)] + parents

@indexer(IAnalysisRequest)
def getParticipantID(instance):
    """Returns the patient ID of the current Analysis Request
    """
    return get_field_value(instance, "ParticipantID", default="")
