# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Botswana Harvard Partnership (BHP)

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from bika.lims.browser.publish.emailview import EmailView as BaseEmailView


class EmailView(BaseEmailView):
    """Email Attachments View
    """
    email_template = ViewPageTemplateFile("templates/email_template.pt")

    def __init__(self, context, request):
        super(EmailView, self).__init__(context, request)
        participant_ids = self.get_participant_ids()
        self.email_subject = "Analysis Results for {}".format(", ".join(participant_ids))

    def get_participant_ids(self):
        """Participant IDs of the reports to be included in the email
        """
        ars = map(lambda rep: rep.getAnalysisRequest(), self.get_reports())
        pids = map(lambda ar: ar.ParticipantID, ars)
        return list(set(pids))

    def get_recipients(self, ar):
        """Returns the recipients the results report must be send to:
        To: client's e-mail (not the contact's e-mail)
        CC: Without CC
        """
        client = ar.getClient()
        email = client.getEmailAddress()
        if not email:
            return []
        return [{
            "UID": "",
            "Fullname": client.Title(),
            "EmailAddress": email,
            "PublicationModes": ("email", "pdf",),
        }]
