# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Botswana Harvard Partnership (BHP)

from Products.Archetypes.Widget import BooleanWidget
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import TextAreaWidget
from Products.Archetypes.references import HoldingReference
from Products.CMFCore.permissions import ModifyPortalContent, View
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from bhp.lims.config import GENDERS
from bika.lims import bikaMessageFactory as _
from bika.lims.browser.widgets import DateTimeWidget
from bika.lims.browser.widgets import SelectionWidget
from bika.lims.browser.widgets.referencewidget import ReferenceWidget
from bika.lims.fields import ExtBooleanField, ExtDateTimeField, \
    ExtReferenceField
from bika.lims.fields import ExtStringField
from bika.lims.fields import ExtTextField
from bika.lims.interfaces import ISample
from zope.component import adapts
from zope.interface import implements


class SampleSchemaExtender(object):
    adapts(ISample)
    implements(IOrderableSchemaExtender)

    def __init__(self, context):
        self.context = context

    fields = [
        ExtStringField(
            "ParticipantID",
            required=1,
            widget=StringWidget(
                label=_("Participant ID"),
                maxlength=22,
                size=22,
                render_own_label=True,
                visible={'edit': 'visible',
                         'view': 'visible',
                         'add': 'edit',
                         'header_table': 'visible'},
            )
        ),

        ExtStringField(
            "OtherParticipantReference",
            required=0,
            widget=StringWidget(
                label=_("Other Participant Ref"),
                maxlength=12,
                size=12,
                render_own_label=True,
                visible={'edit': 'visible',
                         'view': 'visible',
                         'add': 'edit',
                         'header_table': 'visible'},
            )
        ),

        ExtStringField(
            "ParticipantInitials",
            required=1,
            widget=StringWidget(
                label=_("Participant Initials"),
                maxlength=2,
                size=2,
                render_own_label=True,
                visible={'edit': 'visible',
                         'view': 'visible',
                         'add': 'edit',
                         'header_table': 'visible'},
            )
        ),

        ExtStringField(
            "Gender",
            required=1,
            vocabulary=GENDERS,
            widget=SelectionWidget(
                format="radio",
                label=_("Gender"),
                render_own_label=True,
                visible={'edit': 'visible',
                         'view': 'visible',
                         'add': 'edit',
                         'header_table': 'visible'},
            )
        ),

        ExtStringField(
            "Visit",
            required=1,
            widget=StringWidget(
                label=_("Visit Number"),
                maxlength=4,
                size=4,
                render_own_label=True,
                visible={'edit': 'visible',
                         'view': 'visible',
                         'add': 'edit',
                         'header_table': 'visible'},
            )
        ),

        ExtBooleanField(
            "Fasting",
            required=0,
            default=False,
            widget=BooleanWidget(
                format="radio",
                label=_("Fasting"),
                render_own_label=True,
                visible={'edit': 'visible',
                         'view': 'visible',
                         'add': 'edit',
                         'header_table': 'visible'},
            ),
        ),

        ExtDateTimeField(
            'DateOfBirth',
            required=1,
            widget=DateTimeWidget(
                label=_('Date of Birth'),
                datepicker_nofuture=1,
                show_time=False,
                render_own_label=True,
                visible={'edit': 'visible',
                         'view': 'visible',
                         'add': 'edit',
                         'header_table': 'visible'},
            ),
        ),

        ExtStringField(
            "Volume",
            required=1,
            widget=StringWidget(
                label=_("Volume"),
                maxlength=8,
                size=8,
                render_own_label=True,
                visible={'edit': 'visible',
                         'view': 'visible',
                         'add': 'edit',
                         'header_table': 'visible'},
            )
        ),

        ExtTextField(
            "OtherInformation",
            default_content_type="text/plain",
            allowable_content_types=("text/plain",),
            default_output_type="text/plain",
            widget=TextAreaWidget(
                label=_("Other relevant clinical information"),
                render_own_label=True,
                visible={'edit': 'visible',
                         'view': 'visible',
                         'add': 'edit',
                         'header_table': 'visible'},
            ),
        ),

        ExtReferenceField(
            'Courier',
            allowed_types=('Courier'),
            relationship='SampleCourier',
            referenceClass=HoldingReference,
            mode='rw',
            read_permission=View,
            write_permission=ModifyPortalContent,
            widget=ReferenceWidget(
                label=_("Courier"),
                description=_("The courier who delivered this sample"),
                size=20,
                render_own_label=True,
                visible={
                    'view': 'visible',
                    'edit': 'visible',
                    'add': 'invisible',
                    'header_table': 'visible',
                    'secondary': 'disabled',
                    'sample_registered': {'view': 'invisible', 'edit': 'invisible'},
                    'to_be_sampled':     {'view': 'invisible', 'edit': 'invisible'},
                    'scheduled_sampling':{'view': 'invisible', 'edit': 'invisible'},
                    'sampled':           {'view': 'invisible', 'edit': 'invisible'},
                    'to_be_preserved':   {'view': 'invisible', 'edit': 'invisible'},
                    'sample_ordered':    {'view': 'invisible', 'edit': 'invisible'},
                    'sample_due':        {'view': 'visible', 'edit': 'visible'},
                    'sample_prep':       {'view': 'visible', 'edit': 'invisible'},
                    'sample_received':   {'view': 'visible', 'edit': 'invisible'},
                    'attachment_due':    {'view': 'visible', 'edit': 'invisible'},
                    'to_be_verified':    {'view': 'visible', 'edit': 'invisible'},
                    'verified':          {'view': 'visible', 'edit': 'invisible'},
                    'published':         {'view': 'visible', 'edit': 'invisible'},
                    'invalid':           {'view': 'visible', 'edit': 'invisible'},
                    'rejected':          {'view': 'visible', 'edit': 'invisible'},
                },
                catalog_name='bika_setup_catalog',
                base_query={'review_state': 'active'},
                showOn=True,
            )
        ),

        # This Analysis Request is only for internal use?
        # This field is useful when we create Partitions (AR-like), so we don't
        # want the client to see Analysis Requests / Samples that are meant to
        # be used in the lab.
        ExtBooleanField(
            "InternalUse",
            required=0,
            default=False,
            widget=BooleanWidget(
                format="radio",
                label=_("Internal use"),
                render_own_label=True,
                visible={
                    'view': 'visible',
                    'edit': 'invisible',
                    'add': 'invisible',
                    'header_table': 'visible',
                    'secondary': 'disabled',}
            ),
        ),

        ExtReferenceField(
            "PrimarySample",
            multiValue=0,
            allowed_types=("Sample"),
            relationship="SamplePrimarySample",
            referenceClass=HoldingReference,
            mode="rw",
            read_permission=View,
            write_permission=ModifyPortalContent,
            widget=ReferenceWidget(
                label=_("Primary Sample"),
                description=_("The sample this is originated from"),
                size=20,
                render_own_label=True,
                visible={
                    'view': 'visible',
                    'edit': 'invisible',
                    'add': 'invisible',
                    'header_table': 'visible',
                    'secondary': 'disabled',
                },
                catalog_name='bika_catalog',
                base_query={'review_state': 'active'},
                showOn=False,
            ),
        ),
    ]


    def getOrder(self, schematas):
        return schematas

    def getFields(self):
        return self.fields


class SampleSchemaModifier(object):
    adapts(ISample)
    implements(ISchemaModifier)

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        schema['ClientSampleID'].widget.label = _("Client Sample ID (if available)")
        schema['DateSampled'].widget.label = _("Date Time Sampled")
        return schema
