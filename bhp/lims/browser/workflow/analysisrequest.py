# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Botswana Harvard Partnership (BHP)

import tempfile

from DateTime import DateTime
from PyPDF2 import PdfFileMerger
from bhp.lims import api
from bhp.lims import logger
from bika.lims import bikaMessageFactory as _
from bika.lims.browser.workflow import RequestContextAware
from bika.lims.browser.workflow import WorkflowActionGenericAdapter
from bika.lims.interfaces import IWorkflowActionUIDsAdapter
from zope.component.interfaces import implements


class WorkflowActionProcessAdapter(RequestContextAware):
    """Adapter in charge of Analysis Requests 'process' action
    """
    implements(IWorkflowActionUIDsAdapter)

    def __call__(self, action, uids):
        """Redirects the user to the partition magic view
        """
        url = "{}/partition_magic?uids={}".format(self.back_url, ",".join(uids))
        return self.redirect(redirect_url=url)


class WorkflowActionSendToLabAdapter(RequestContextAware):
    """Adapter in charge of Analysis Request "send_to_lab" action
    """
    implements(IWorkflowActionUIDsAdapter)

    def __call__(self, action, uids):
        """Redirects the user to the courier shipment view
        """
        uids = ",".join(uids)
        url = "{}/courier_shipment?uids={}".format(self.back_url, uids)
        return self.redirect(redirect_url=url)

class WorkflowActionSendToPotAdapter(RequestContextAware):
    """Adapter in charge of Analysis Request "send_to_pot" action
    """
    implements(IWorkflowActionUIDsAdapter)

    def __call__(self, action, uids):
        """Redirects the user to the point of testing shipment view
        """
        uids = ",".join(uids)
        url = "{}/pot_shipment?uids={}".format(self.back_url, uids)
        return self.redirect(redirect_url=url)


class WorkflowActionMergedPDFs(WorkflowActionGenericAdapter):

    def __call__(self, action, objects):

        """Generates a pdf with last requisition pdfs generated for the passed
        in objects and returns the pdf through the request.
        """
        files_names = map(self.get_pdf, objects)
        files_names = filter(None, files_names)
        if not files_names:
            ids = ", ".join(map(api.get_id, objects))
            message = _("No PDFs found for {}").format(ids)
            return self.redirect(message=message, level="warning")

        # Merge the pdfs into one single file
        pdf = self.merge_pdfs(files_names)

        # Deliver the pdf
        return self.response_pdf(pdf)

    def get_pdf(self, analysis_request):
        return None

    def get_last_attachment_pdf(self, analysis_request, attachment_type):
        """Returns the last attachment from the analysis_request passed in that
        matches with the attachment_type specified
        """
        last_attachment = None
        attachments = analysis_request.getAttachment()
        for attachment in attachments:
            att_type = attachment.getAttachmentType()
            if not att_type:
                continue
            if att_type.Title() == attachment_type:
                last_attachment = attachment
        if last_attachment:
            attachment_file = last_attachment.getAttachmentFile()
            try:
                return self.write_tmp_pdf(attachment_file)
            except Exception as err_msg:
                logger.error("Cannot get data from attachment for {}: {}"
                             .format(api.get_id(analysis_request), err_msg))
        return None

    def merge_pdfs(self, files):
        """Merges multiple pdfs into one single temporary pdf and returns its
        full path
        """
        merger = PdfFileMerger()
        for pdf in files:
            merger.append(pdf)

        tmp = tempfile.mktemp()
        with open(tmp, 'wb') as fout:
            merger.write(fout)
        return tmp

    def write_tmp_pdf(self, attachment_file):
        """Writes a temporary file with .pdf extension with the contents of the
        attachment passed in and returns the full path of the output file
        """
        if not attachment_file:
            return None
        outfile, outfilename = tempfile.mkstemp(suffix=".pdf")
        outfile = open(outfilename, 'wb')
        outfile.write(str(attachment_file.data))
        outfile.close()
        return outfilename

    def response_pdf(self, filename):
        """Generates a valid http response for the pdf
        """
        now = DateTime()
        nice_filename = '%s_%s' % (filename, now.strftime('%Y%m%d'))
        self.request.response.setHeader("Content-Type", "application/pdf")
        self.request.response.setHeader("Content-Disposition", "attachment")
        self.request.response.setHeader("filename", nice_filename)
        self.request.response.setHeader('Last-Modified',
                                        DateTime.rfc822(DateTime()))
        self.request.response.setHeader("Cache-Control", "no-store")
        self.request.response.setHeader("Pragma", "no-cache")
        return open(filename, 'rb').read()


class WorkflowActionDownloadRequisitionAdapter(WorkflowActionMergedPDFs):
    """Adapter in charge of "download_requisition"'s custom action
    """

    def get_pdf(self, analysis_request):
        """Returns the full path of last requisition report (pdf) that was
        generated for the Analysis Request passed in
        """
        return self.get_last_attachment_pdf(analysis_request, "Requisition")


class WorkflowActionDownloadDeliveryAdapter(WorkflowActionMergedPDFs):
    """Adapter in charge of "download_delivery"'s custom action
    """

    def get_pdf(self, analysis_request):
        """Returns the full path of last delivery report (pdf) that was
        generated for the Analysis Request passed in
        """
        return self.get_last_attachment_pdf(analysis_request, "Delivery")
