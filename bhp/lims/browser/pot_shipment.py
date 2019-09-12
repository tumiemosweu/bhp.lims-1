# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Botswana Harvard Partnership (BHP)

from collections import OrderedDict

from DateTime import DateTime
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from bhp.lims import api
from bhp.lims import bhpMessageFactory as _
from bhp.lims import logger
from bhp.lims.browser.internal_delivery import generate_internal_delivery_pdf
from bika.lims import workflow as wf

ALLOWED_STATES = ["sample_at_reception"]


class POTShipmentView(BrowserView):
    """Assign a lab contact to ARs and submit it to the lab
    """
    template = ViewPageTemplateFile("templates/pot_shipment.pt")

    def __init__(self, context, request):
        super(POTShipmentView, self).__init__(context, request)
        self.context = context
        self.request = request
        self.back_url = self.context.absolute_url()
        self.redirect_url = ""

    def __call__(self):
        form = self.request.form
        form_submitted = form.get("submitted", False)
        form_send = form.get("send", False)
        form_cancel = form.get("cancel", False)
        objs = self.get_objects()

        if not objs:
            return self.redirect(message=_("No items selected"))

        # Handle form submit
        if form_submitted and form_send:
            logger.info("*** SEND TO POINT OF TESTING ***")
            lab_contact_uid = form.get("lab_contact")
            lab_contact = self.get_object_by_uid(lab_contact_uid)
            lab_department_uid = form.get("lab_department")
            lab_department = self.get_object_by_uid(lab_department_uid)

            if lab_contact is None:
                return self.redirect(message=_("No lab contact selected"))

            if lab_department is None:
                return self.redirect(message=_("No department selected"))

            sent_objects = []
            sent_object_ids = []
            for obj in objs:
                logger.info("*** SENDING {} TO POINT OF TESTING ***".format(obj.getId()))
                if self.send_to_pot(obj, lab_contact):
                    sent_objects.append(obj)

            sent_object_ids = map(lambda obj: obj.getId(), sent_objects)
            message = None
            if sent_object_ids:
                message = _("Sent {} to point of testing".format(
                    ", ".join(sent_object_ids)))

                # TODO Redirect the user to back_url while downloading pdf

                # Generate the delivery report
                pdf = generate_internal_delivery_pdf(self.context, sent_objects, lab_department)
                return self.response_pdf(pdf)

            else:
                message = _("All items have been already sent to point of testing".format(
                    ", ".join(sent_object_ids)))
            return self.redirect(message=message, level="info")

        # Handle form cancel
        if form_submitted and form_cancel:
            logger.info("*** CANCEL ***")
            return self.redirect(message=_("Delivery canceled"))

        # render the template
        return self.template()

    def send_to_pot(self, ar, lab_contact):
        """Set the lab_contact and send the AR to the lab
        """
        # Only proceed if the AR is in an allowed state
        if api.get_workflow_status_of(ar) not in ALLOWED_STATES:
            logger.info("Skipping already sent to point of testing AR {}".format(ar.getId()))
            return False

        # 1. Set the lab_contact to the extended field
        ar.getField("LabContact").set(ar, lab_contact)

        # 2. Transition the AR to due
        wf.doActionFor(ar, "send_to_pot")

        return True

    def redirect(self, redirect_url=None, message=None, level="warning"):
        """Redirect with a message
        """
        if redirect_url is None:
            redirect_url = self.back_url
        if message is not None:
            self.add_status_message(message, level)
        return self.request.response.redirect(redirect_url)

    def get_lab_contacts(self):
        """Return all lab contacts
        """
        query = {
            "portal_type": "LabContact",
            "sort_on": "sortable_title",
            "sort_order": "ascending",
        }
        results = api.search(query)
        return map(api.get_object, results)

    def get_lab_contacts_data(self):
        """Returns a list of lab contacts data
        """
        for obj in self.get_lab_contacts():
            info = self.get_base_info(obj)
            yield info

    def get_lab_departments(self):
        """Return all lab departments
        """
        query = {
            "portal_type": "Department",
            "sort_on": "sortable_title",
            "sort_order": "ascending",
        }
        results = api.search(query)
        return map(api.get_object, results)

    def get_lab_departments_data(self):
        """Returns a list of lab departments data
        """
        for obj in self.get_lab_departments():
            info = self.get_base_info(obj)
            yield info

    def get_objects(self):
        """Returns a list of objects coming from the "uids" request parameter
        """
        # Create a mapping of source ARs for copy
        uids = self.request.form.get("uids", "")
        if not uids:
            uids = self.request.form.get("items", "")
            uids = uids.split(',')
        # handle 'uids' GET parameter coming from a redirect
        if isinstance(uids, basestring):
            uids = uids.split(",")
        unique_uids = OrderedDict().fromkeys(uids).keys()
        return filter(None, map(self.get_object_by_uid, unique_uids))

    def get_base_info(self, obj):
        """Extract the base info from the given object
        """
        review_state = api.get_workflow_status_of(obj)
        state_title = review_state.capitalize().replace("_", " ")
        return {
            "obj": obj,
            "id": api.get_id(obj),
            "uid": api.get_uid(obj),
            "title": api.get_title(obj),
            "path": api.get_path(obj),
            "url": api.get_url(obj),
            "review_state": review_state,
            "state_title": state_title,
        }

    def get_ar_data(self):
        """Returns a list of AR data
        """
        for obj in self.get_objects():
            info = self.get_base_info(obj)
            yield info

    def get_object_by_uid(self, uid):
        """Get the object by UID
        """
        logger.debug("get_object_by_uid::UID={}".format(uid))
        obj = api.get_object_by_uid(uid, None)
        if obj is None:
            logger.warn("!! No object found for UID #{} !!")
        return obj

    def add_status_message(self, message, level="info"):
        """Set a portal status message
        """
        return self.context.plone_utils.addPortalMessage(message, level)

    def response_pdf(self, filename):
        now = DateTime()
        nice_filename = '%s_%s' % (filename, now.strftime('%Y%m%d'))
        self.request.response.setHeader("Content-Type", "application/pdf")
        self.request.response.setHeader("Content-Disposition", "download")
        self.request.response.setHeader("filename", nice_filename)
        self.request.response.setHeader('Last-Modified',
                                        DateTime.rfc822(DateTime()))
        self.request.response.setHeader("Cache-Control", "no-store")
        self.request.response.setHeader("Pragma", "no-cache")
        return open(filename, 'rb').read()
