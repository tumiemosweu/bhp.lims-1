# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Botswana Harvard Partnership (BHP)

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from bhp.lims import api
from bhp.lims import bhpMessageFactory as _
from bhp.lims import logger
from bika.lims.browser.analysisrequest import \
    AnalysisRequestAnalysesView as BaseAnalysesView
from bika.lims.browser.analysisrequest import \
    AnalysisRequestManageResultsView as BaseManageResultsView
from bika.lims.browser.analysisrequest import \
    AnalysisRequestPublishedResults as BasePublishedResultsView
from bika.lims.browser.analysisrequest import AnalysisRequestViewView
from bika.lims.interfaces import IAnalysisRequest
from bika.lims.utils import encode_header
from email.Utils import formataddr


def handle_email_panic(view):
    # If the email for panic levels has been submitted, send the email
    if "email_popup_submit" in view.request:
        if send_panic_email(view):
            ar_uid = api.get_uid(view.context)
            url = "{}/analysisrequests/publish?items={}".format(view.portal_url,
                                                                ar_uid)
            return view.request.response.redirect(url)


def send_panic_email(view):
    ar = view.context
    if not IAnalysisRequest.providedBy(ar):
        return False

    if not ar.has_analyses_in_panic():
        addMessage(view, _("No results exceed the panic levels"), 'warning')
        return False

    # Send an alert email
    laboratory = view.context.bika_setup.laboratory
    subject = view.request.get('subject')
    to = view.request.get('to')
    body = view.request.get('email_body')
    body = "<br/>".join(body.split("\r\n"))
    mime_msg = MIMEMultipart('related')
    mime_msg['Subject'] = subject
    mime_msg['From'] = formataddr(
        (encode_header(laboratory.getName()),
         laboratory.getEmailAddress()))
    mime_msg['To'] = to
    msg_txt = MIMEText(safe_unicode(body).encode('utf-8'), _subtype='html')
    mime_msg.preamble = 'This is a multi-part MIME message.'
    mime_msg.attach(msg_txt)
    try:
        host = getToolByName(view.context, 'MailHost')
        host.send(mime_msg.as_string(), immediate=True)
    except Exception, msg:
        ar = view.context.id
        logger.error("Panic level email %s: %s" % (ar, str(msg)))
        message = _('Unable to send an email to alert client '
                    'that some results exceeded the panic levels') \
                  + (": %s" % str(msg))
        addMessage(view, message, 'warning')
        return False
    api.set_field_value(view.context, "PanicEmailAlertSent", True)
    return True


def addMessage(view, message, msg_type="info"):
    view.context.plone_utils.addPortalMessage(message, msg_type)


class AnalysisRequestView(AnalysisRequestViewView):

    def __call__(self):
        template = super(AnalysisRequestView, self).__call__()
        if not handle_email_panic(self):
            return template


class AnalysisRequestAnalysesView(BaseAnalysesView):

    def __call__(self):
        template = super(AnalysisRequestAnalysesView, self).__call__()
        handle_email_panic(self)
        return template


class AnalysisRequestManageResultsView(BaseManageResultsView):

    def __call__(self):
        template = super(AnalysisRequestManageResultsView, self).__call__()
        handle_email_panic(self)
        return template


class AnalysisRequestPublishedResultsView(BasePublishedResultsView):

    def __call__(self):
        template = super(AnalysisRequestPublishedResultsView, self).__call__()
        handle_email_panic(self)
        return template

