# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Botswana Harvard Partnership (BHP)

from DateTime import DateTime
from Products.ATContentTypes.utils import DT2dt
from bhp.lims import api
from bika.lims.alphanumber import Alphanumber
from bika.lims.idserver import AR_TYPES
from bika.lims.idserver import get_current_year
from bika.lims.idserver import get_partition_count
from bika.lims.idserver import get_retest_count
from bika.lims.idserver import get_secondary_count
from bika.lims.idserver import get_type_id
from bika.lims.idserver import strip_suffix


def get_variables(context, **kw):
    """Prepares a dictionary of key->value pairs usable for ID formatting
    """
    # allow portal_type override
    portal_type = get_type_id(context, **kw)

    # The variables map hold the values that might get into the constructed id
    variables = {
        'context': context,
        'id': api.get_id(context),
        'portal_type': portal_type,
        'year': get_current_year(),
        'parent': api.get_parent(context),
        'seq': 0,
        'alpha': Alphanumber(0),
    }

    # Augment the variables map depending on the portal type
    if portal_type in AR_TYPES:
        now = DateTime()
        sampling_date = context.getSamplingDate()
        sampling_date = sampling_date and DT2dt(sampling_date) or DT2dt(now)
        date_sampled = context.getDateSampled()
        date_sampled = date_sampled and DT2dt(date_sampled) or DT2dt(now)
        test_count = 1

        variables.update({
            "clientId": context.getClientID(),
            "dateSampled": date_sampled,
            "samplingDate": sampling_date,
            "sampleType": context.getSampleType().getPrefix(),
            "test_count": test_count,
            # BHP-specific
            "studyId": context.aq_parent.getTaxNumber(),
        })

        # Partition
        if portal_type == "AnalysisRequestPartition":
            parent_ar = context.getParentAnalysisRequest()
            parent_ar_id = api.get_id(parent_ar)
            parent_base_id = strip_suffix(parent_ar_id)
            partition_count = get_partition_count(context)
            variables.update({
                "parent_analysisrequest": parent_ar,
                "parent_ar_id": parent_ar_id,
                "parent_base_id": parent_base_id,
                # BHP-specific
                "partition_count": "{:02d}".format(partition_count+1),
                "parent_alpha": get_sample_alpha(parent_ar),
            })

        # Retest
        elif portal_type == "AnalysisRequestRetest":
            # Note: we use "parent" instead of "invalidated" for simplicity
            parent_ar = context.getInvalidated()
            parent_ar_id = api.get_id(parent_ar)
            parent_base_id = strip_suffix(parent_ar_id)
            # keep the full ID if the retracted AR is a partition
            if context.isPartition():
                parent_base_id = parent_ar_id
            retest_count = get_retest_count(context)
            test_count = test_count + retest_count
            variables.update({
                "parent_analysisrequest": parent_ar,
                "parent_ar_id": parent_ar_id,
                "parent_base_id": parent_base_id,
                "retest_count": retest_count,
                "test_count": test_count,
            })

        # Secondary
        elif portal_type == "AnalysisRequestSecondary":
            primary_ar = context.getPrimaryAnalysisRequest()
            primary_ar_id = api.get_id(primary_ar)
            parent_base_id = strip_suffix(primary_ar_id)
            secondary_count = get_secondary_count(context)
            variables.update({
                "parent_analysisrequest": primary_ar,
                "parent_ar_id": primary_ar_id,
                "parent_base_id": parent_base_id,
                "secondary_count": secondary_count,
            })

    elif portal_type == "ARReport":
        variables.update({
            "clientId": context.aq_parent.getClientID(),
        })

    return variables


def get_sample_alpha(sample):
    """Returns the alpha part of a sample id when the format id for the
    given sample matches with '{studyId}{sampleType}{alpha:3a2d}{test_count}'
    """
    sample_id = api.get_id(sample)
    study_id = sample.aq_parent.getTaxNumber()
    sample_type = sample.getSampleType().getPrefix()
    prefix = "{}{}".format(study_id, sample_type)
    len_prefix = len(prefix)
    return sample_id[len_prefix:len_prefix+5]
