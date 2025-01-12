# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Botswana Harvard Partnership (BHP)

from AccessControl import ClassSecurityInfo
from Products.Archetypes.Registry import registerWidget
from bhp.lims.config import GRADES_KEYS
from bhp.lims.browser.analysisspecification import AnalysisSpecificationView
from bika.lims.browser.widgets.analysisspecificationwidget import \
    AnalysisSpecificationWidget as BaseWidget


class AnalysisSpecificationWidget(BaseWidget):
    _properties = BaseWidget._properties.copy()
    security = ClassSecurityInfo()

    @security.public
    def process_form(self, instance, field, form, empty_marker=None,
                     emptyReturnsMarker=False):
        """Return a list of dictionaries fit for AnalysisSpecsResultsField
           consumption.

        If neither hidemin nor hidemax are specified, only services which have
        float()able entries in result,min and max field will be included. If
        hidemin and/or hidemax specified, results might contain empty min
        and/or max fields.
        """
        values, outdict = BaseWidget.process_form(self, instance=instance,
            field=field, form=form, empty_marker=empty_marker,
            emptyReturnsMarker=emptyReturnsMarker
        )

        for index in range(len(values)):
            item = values[index]
            uid = item["uid"]
            min_panic = self._get_spec_value(form, uid, "minpanic")
            max_panic = self._get_spec_value(form, uid, "maxpanic")
            s_calc = self._get_spec_value(form, uid, "calculation",
                                          check_floatable=False)
            values[index]["minpanic"] = min_panic
            values[index]["maxpanic"] = max_panic
            values[index]["calculation"] = s_calc

            # Grades
            for grade in GRADES_KEYS:
                grade_val = self._get_spec_value(form, uid, grade)
                values[index][grade] = grade_val

        return values, outdict

    @security.public
    def AnalysisSpecificationResults(self, field, allow_edit=False):
        """Render listing with categorized services.

        :param field: Contains the schema field with a list of services in it
        """
        fieldvalue = getattr(field, field.accessor)()

        # N.B. we do not want to pass the field as the context to
        # AnalysisProfileAnalysesView, but rather the holding instance
        instance = getattr(self, "instance", field.aq_parent)
        view = AnalysisSpecificationView(instance,
                                         self.REQUEST,
                                         fieldvalue=fieldvalue,
                                         allow_edit=allow_edit)

        return view.contents_table(table_only=True)

registerWidget(AnalysisSpecificationWidget,
               title='Analysis Specification Results',
               description=('Analysis Specification Results'))
