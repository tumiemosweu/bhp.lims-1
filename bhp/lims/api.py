# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Botswana Harvard Partnership (BHP)

import sys
from Products.ATContentTypes.utils import DT2dt
from bhp.lims import logger
from bhp.lims.config import GRADES_KEYS
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
    """Returns a tuple with the year, month and days for a given age in passed
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


def get_unit(volume_unit, default=""):
    """Returns the unit string from the value passed in, if any
    """
    if not volume_unit:
        return default
    unit = volume_unit.replace(get_leading_number(volume_unit), "").strip()
    return unit or default


def get_volume(volume_unit, default=0):
    """Returns the volume (decimal) from the value passed in
    """
    number = get_leading_number(volume_unit)
    if not number:
        return default
    return to_float(number)


def get_leading_number(value):
    if not value:
        return ""

    val_str = ""
    for val in list(value.strip()):
        tmp_val = "{}{}".format(val_str, val)
        if not is_floatable(tmp_val):
            if val_str:
                break
            if val not in [".", "-"]:
                break
        val_str = tmp_val
    return val_str.strip()


def is_in_panic(brain_or_object):
    """Returns true if the result for the analysis passed in is within any of
    the intervals defined for the minimum grade level the panic alert is
    configured for.
    """
    grade_cutoff = 3
    grade = get_grade_number(brain_or_object)
    if grade >= grade_cutoff:
        return True
    return False


def get_grades_numbers():
    """Returns a list with the available grade numbers/indexes
    """
    grades = list()
    for grade in GRADES_KEYS:
        grade_idx = int(grade.split("_")[0].replace("G", ""))
        grades.append(grade_idx)
    return list(set(grades))


def get_grade_number(brain_or_object):
    """Return the result grade the result of the analysis falls in. If the
    result does not fail within any grade range, returns None
    """
    for grade in get_grades_numbers():
        if is_in_grade_range(brain_or_object, grade):
            return grade
    return None


def is_in_grade_range(brain_or_object, grade, level=None):
    """Returns whether the result is within the specified grade index and level
    """
    if not level:
        if is_in_grade_range(brain_or_object, grade, level="low"):
            return True
        if is_in_grade_range(brain_or_object, grade, level="high"):
            return True
        return False

    result = safe_getattr(brain_or_object, "getResult", None)
    if not is_floatable(result):
        return False

    result_range = safe_getattr(brain_or_object, "getResultsRange", None)
    if not result_range:
        return False

    grade_min_key = "G{}_{}_min".format(grade, level)
    grade_min = result_range.get(grade_min_key, "")
    if not is_floatable(grade_min):
        if min(get_grades_numbers()) != grade:
            return False
        grade_min = -sys.maxint - 1

    grade_low_max_key = "G{}_{}_max".format(grade, level)
    grade_max = result_range.get(grade_low_max_key, "")
    if not is_floatable(grade_max):
        if max(get_grades_numbers()) != grade:
            return False
        grade_max = sys.maxint

    result = to_float(result)
    if result >= to_float(grade_min) and result <= to_float(grade_max):
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
