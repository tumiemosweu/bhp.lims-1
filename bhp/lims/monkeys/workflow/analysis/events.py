from bika.lims.interfaces.analysis import IRequestAnalysis
from bika.lims.workflow import doActionFor
from bhp.lims.api import set_field_value


def after_submit(obj):
    ws = obj.getWorksheet()
    if ws:
        doActionFor(ws, 'submit')

    if IRequestAnalysis.providedBy(obj):
        ar = obj.getRequest()
        set_field_value(ar, "AssayDate", obj.getDateSubmitted())
        doActionFor(ar, 'submit')
