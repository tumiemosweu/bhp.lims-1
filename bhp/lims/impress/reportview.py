# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Botswana Harvard Partnership (BHP)

from bhp.lims import api
from bhp.lims import logger
from bika.lims.workflow import getTransitionDate
from senaite.impress.analysisrequest.reportview import MultiReportView
from senaite.impress.analysisrequest.reportview import SingleReportView


class BhpSingleReportView(SingleReportView):
    """BHP specific controller view for single-reports
    """

    def __init__(self, model, request):
        logger.info("BhpSingleReportView::__init__:model={}"
                    .format(model))
        super(BhpSingleReportView, self).__init__(model, request)

    def get_age_str(self, model):
        years, months, days = api.get_age(model.DateOfBirth, model.DateSampled)
        years = years and "{}y".format(years) or None
        months = months and "{}m".format(months) or None
        days = days and "{}d".format(days) or None
        age = filter(lambda val: val != None, [years, months, days])
        return " ".join(age)

    def is_floatable(self, result):
        """Returns whether the result is floatable or not
        """
        return api.is_floatable(result)

    def to_float(self, result):
        """Returns the floatable result
        """
        return api.to_float(result)

    def get_grade_html(self, analysis):
        """Returns an html representation (span) of the grade range the result
        of the analysis falls in, if any. Otherwise, returns None
        """
        grade_idx = api.get_grade_number(analysis)
        if not grade_idx:
            return None
        return "<span class='grade_{}'>G{}</span>".format(grade_idx, grade_idx)

    def get_referral_labs_data(self, sample):
        """Returns a dictionary with the data to be displayed if one or more
        analyses were tested by a referral lab
        """
        data = {}
        for analysis in sample.getAnalyses(full_objects=True):
            ref_lab = api.get_field_value(analysis, "ReferralLab", None)
            if ref_lab:
                title = api.get_title(ref_lab)
                stored = data.get(title, [])
                stored.append(api.get_title(analysis))
                data.update({title: stored})
        return data


class BhpMultiReportView(MultiReportView):
    """BHP specific controller view for multi-reports
    """

    def __init__(self, collection, request):
        logger.info("BhpMultiReportView::__init__:collection={}"
                    .format(collection))
        super(BhpMultiReportView, self).__init__(collection, request)

    def get_transition_date(self, obj, transition=None):
        """Returns the date of the given Transition
        """
        if transition is None:
            return None
        return getTransitionDate(obj, transition, return_as_datetime=True)

    def is_floatable(self, result):
        """Returns whether the result is floatable or not
        """
        return api.is_floatable(result)

    def to_float(self, result):
        """Returns the floatable result
        """
        return api.to_float(result)

    def get_grade_html(self, analysis):
        """Returns an html representation (span) of the grade range the result
        of the analysis falls in, if any. Otherwise, returns None
        """
        grade_idx = api.get_grade_number(analysis)
        if not grade_idx:
            return None
        return "<span class='grade_{}'>G{}</span>".format(grade_idx, grade_idx)
