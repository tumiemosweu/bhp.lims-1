# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Botswana Harvard Partnership (BHP)

import tempfile
from base64 import b64encode

from Products.CMFPlone.utils import _createObjectByType
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from barcode import Code39
from barcode.writer import ImageWriter
from bhp.lims import api
from bhp.lims import logger
from bika.lims.browser import BrowserView
from bika.lims.idserver import renameAfterCreation
from bika.lims.interfaces import IAnalysisRequest, ISample
from bika.lims.utils import createPdf


class InternalDeliveryFormPdf(BrowserView):
    template = ViewPageTemplateFile("templates/internal_delivery.pt")

    def __init__(self, context, request, analysis_requests=None, lab_department=None):
        super(InternalDeliveryFormPdf, self).__init__(context, request)

        self.analysis_requests = analysis_requests
        self.lab_department = lab_department
        if not self.analysis_requests:
            if ISample.providedBy(context):
                self.analysis_requests = context.getAnalysisRequests()
            elif IAnalysisRequest.providedBy(context):
                self.analysis_requests = [context]

    def __call__(self):
        return self.template()

    def get(self, instance, field_name):
        return instance.Schema().getField(field_name).get(instance)

    def get_contact_name(self):
        user = api.get_current_user()
        contact = api.get_user_contact(user)
        return contact.getFullname()

    def get_barcode(self, instance):
        ean = Code39(u''+str(instance.id), writer=ImageWriter())
        ean.default_writer_options.update(font_size=20)
        barcode_img = tempfile.mktemp(suffix='.png')
        localFile = open(barcode_img, 'w')
        ean.write(localFile)
        localFile.close()
        img = open(barcode_img, 'r')
        img_str = img.read()
        return "data:image/png;base64,{}".format(b64encode(img_str))

def generate_internal_delivery_pdf(context, ars_or_samples, lab_department):

    if not ars_or_samples:
        logger.warn("No Analysis Requests or Samples provided")
        return

    if ISample.providedBy(ars_or_samples) or \
        IAnalysisRequest.providedBy(ars_or_samples):
        return generate_internal_delivery_pdf(context, [ars_or_samples], lab_department)

    if not isinstance(ars_or_samples, list):
        logger.warn("Type not supported: {}".format(repr(ars_or_samples)))
        return

    html = InternalDeliveryFormPdf(context, context.REQUEST,
                           analysis_requests=ars_or_samples, lab_department=lab_department).template()
    html = safe_unicode(html).encode("utf-8")
    filename = "internal_delivery"
    pdf_fn = tempfile.mktemp(suffix=".pdf")
    pdf = createPdf(htmlreport=html, outfile=pdf_fn)
    if not pdf:
        ar_ids = map(lambda ar: ar.id, ars_or_samples)
        logger.warn("Unable to generate the PDF of internal delivery form for {}".
                    format(' '.join(ar_ids)))
        return None

    def _attach_to_ar(pdf, ar_brain_or_obj):
        ar = api.get_object(ar_brain_or_obj)

        # Attach the pdf to the Analysis Request
        attid = ar.aq_parent.generateUniqueId('Attachment')
        att = _createObjectByType(
            "Attachment", ar.aq_parent, attid)
        att.setAttachmentFile(open(pdf_fn))
        att.setReportOption('i')  # Ignore in report

        # Try to assign the Requisition Attachment Type
        query = dict(portal_type='AttachmentType', title='Delivery')
        brains = api.search(query, 'bika_setup_catalog')
        if brains:
            att_type = api.get_object(brains[0])
            att.setAttachmentType(att_type)

        # Awkward workaround to rename the file
        attf = att.getAttachmentFile()
        attf.filename = '%s.pdf' % filename
        att.setAttachmentFile(attf)
        att.unmarkCreationFlag()
        renameAfterCreation(att)
        atts = ar.getAttachment() + [att] if ar.getAttachment() else [att]
        atts = [a.UID() for a in atts]
        ar.setAttachment(atts)

    # TODO Create only one Attachment per Client and assign it to all ARs
    # There is no need to creat a single Attachment object for each AR. Same
    # attachment can be assigned to different ARs and they will resolve the
    # attachment correctly later. This will be useful for:
    # a) Reduce the database size (less pdfs to store)
    # b) workflow_download_delivery can easily return the attachments that are
    #    different when multiple ARs are selected.

    for ar_or_sample in ars_or_samples:
        # Attach the pdf to the Analysis Request
        if ISample.providedBy(ar_or_sample):
            for ar in ar_or_sample.getAnalysisRequests():
                _attach_to_ar(pdf, ar)
        elif IAnalysisRequest.providedBy(ar_or_sample):
            _attach_to_ar(pdf, ar_or_sample)

    return pdf_fn
