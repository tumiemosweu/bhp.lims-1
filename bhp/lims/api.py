# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Botswana Harvard Partnership (BHP)

from Products.ATContentTypes.utils import DT2dt
from bhp.lims import logger
from bika.lims.api import *
from bika.lims.utils import render_html_attributes
from dateutil.relativedelta import relativedelta

_marker = object()


def get_field_value(instance, field_name, default=_marker):
    """Returns the value of a Schema field from the instance passed in
    """
    instance = get_object(instance)
    field = instance.Schema() and instance.Schema().getField(field_name) or None
    if not field:
        if default is not _marker:
            return default
        fail("No field {} found for {}".format(field_name, repr(instance)))
    return instance.Schema().getField(field_name).get(instance)


def set_field_value(instance, field_name, value):
    """Sets the value to a Schema field
    """
    if field_name == "id":
        logger.warn("Assignment of id is not allowed")
        return
    logger.info("Field {} = {}".format(field_name, repr(value)))
    instance = get_object(instance)
    field = instance.Schema() and instance.Schema().getField(field_name) or None
    if not field:
        fail("No field {} found for {}".format(field_name, repr(instance)))
    field.set(instance, value)


def get_age(datetime_from, datetime_to=None):
    """Returns the elapsed time in years, months and days between the two
    dates passed in."""
    if not datetime_to:
        datetime_to = DateTime()

    if not is_date(datetime_from) or not is_date(datetime_to):
        fail("Only DateTime and datetype types are supported")


    dfrom = DT2dt(to_date(datetime_from)).replace(tzinfo=None)
    dto = DT2dt(to_date(datetime_to)).replace(tzinfo=None)

    diff = relativedelta(dto, dfrom)
    return (diff.years, diff.months, diff.days)


def to_age_str(years=0, months=0, days=0):
    """Returns a string representation of an age
    """
    if not is_floatable(years):
        fail("Years are not floatable")
    if not is_floatable(months):
        fail("Months are not floatabla")
    if not is_floatable(days):
        fail("Days are not floatable")

    age_arr = list()
    if years:
        age_arr.append("{}y".format(years))
    if months:
        age_arr.append("{}m".format(months))
    if days:
        age_arr.append("{}d".format(days))
    return ' '.join(age_arr)


def to_age(age):
    """Returns  a tuple with the year, month and days for a given age in passed
    in as string format
    """
    def get_age_value(age_str, age_key):
        regex = '(\d+){}'.format(age_key)
        matches = re.findall(regex, age)
        if not matches:
            return 0
        age_val = matches[0]
        if age_val and is_floatable(age_val):
            return age_val.strip()
        return 0

    years = get_age_value(age, 'y')
    months = get_age_value(age, 'm')
    days = get_age_value(age, 'd')
    return (years, months, days)


def is_in_panic(brain_or_object):
    """Returns true if the result for the analysis passed in is equal or below
    the min panic or equal or above max panic
    """
    result = safe_getattr(brain_or_object, "getResult", None)
    if not is_floatable(result):
        return False

    result_range = safe_getattr(brain_or_object, "getResultsRange", None)
    if not result_range:
        return False

    # Out of range. Check if minpanic or maxpanic are set
    result = to_float(result)
    panic_min = result_range.get('minpanic', "")
    panic_max = result_range.get('maxpanic', "")
    panic_min = is_floatable(panic_min) and panic_min or None
    panic_max = is_floatable(panic_max) and panic_max or None

    if panic_min is not None and result <= panic_min:
        return True

    if panic_max is not None and result >= panic_max:
        return True
    return False


def is_client_contact():
    """Returns whether the current user is a Client contact
    """
    return get_current_client() is not None


def get_html_image(name, **kwargs):
    """Returns a well-formed img html
    :param name: file name of the image
    :param kwargs: additional attributes and values
    :return: a well-formed html img
    """
    if not name:
        return ""
    portal_url = get_url(get_portal())
    attr = render_html_attributes(**kwargs)
    html = '<img src="{}/++resource++bhp.lims.static/images/{}" {}/>'
    return html.format(portal_url, name, attr)
