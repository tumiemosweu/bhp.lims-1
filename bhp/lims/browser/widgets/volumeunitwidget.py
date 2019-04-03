# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Botswana Harvard Partnership (BHP)

from AccessControl import ClassSecurityInfo
from Products.Archetypes.Registry import registerWidget
from Products.Archetypes.Widget import StringWidget
from bhp.lims import api


class VolumeUnitWidget(StringWidget):
    security = ClassSecurityInfo()
    _properties = StringWidget._properties.copy()
    _properties.update({
        "macro": "volumeunit",
        "size": 10,
    })

    @security.public
    def process_form(self, instance, field, form, empty_marker=None,
                     emptyReturnsMarker=False, validating=True):
        field_name = field.getName()
        volume = form.get("{}_volume".format(field_name), "")
        unit = form.get("{}_unit".format(field_name), "")
        value = "{} {}".format(volume, unit).strip()

        if value is empty_marker:
            return empty_marker

        if emptyReturnsMarker and value == "":
            return empty_marker

        return value, {}

    def get_unit(self, vocabulary, raw_value):
        unit = api.get_unit(raw_value).strip()
        if unit not in vocabulary.keys():
            return ""
        return unit

    def get_volume(self, raw_value):
        return api.get_leading_number(raw_value).strip()


registerWidget(VolumeUnitWidget,
               title="VolumeUnit",
               description=("Renders and input HTML element for volume entry,"
                            "together with a selection list for unit"),)
