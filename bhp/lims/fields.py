# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Botswana Harvard Partnership (BHP)

from Products.Archetypes.Registry import registerField
from bhp.lims import api
from bika.lims.fields import ExtStringField


class VolumeUnitField(ExtStringField):

    def set(self, instance, value, **kwargs):
        original = instance.__dict__.get(self.getName(), "")
        original_unit = api.get_unit(original)
        original_volume = api.get_leading_number(original)

        new_unit = api.get_unit(value, default=original_unit)
        new_vol = api.get_leading_number(value) or original_volume
        new_value = "{} {}".format(new_vol, new_unit)

        super(VolumeUnitField, self).set(instance, new_value, **kwargs)


registerField(VolumeUnitField,
              title="VolumeUnit",
              description="Used for storing volume units", )
