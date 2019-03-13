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
from bhp.lims.config import PRIORITIES
from bika.lims import bikaMessageFactory as _
from bika.lims.browser.widgets import DateTimeWidget
from bika.lims.browser.widgets import SelectionWidget
from bika.lims.browser.widgets.referencewidget import ReferenceWidget
from bika.lims.fields import ExtBooleanField
from bika.lims.fields import ExtDateTimeField
from bika.lims.fields import ExtReferenceField
from bika.lims.fields import ExtStringField
from bika.lims.fields import ExtTextField
from bika.lims.interfaces import IAnalysisRequest
from zope.component import adapts
from zope.interface import implements

fields = [
    ExtStringField(
        "ParticipantID",
        mode="rw",
        required=1,
        read_permission=View,
        write_permission=ModifyPortalContent,
        widget=StringWidget(
            label=_("Participant ID"),
            maxlength=22,
            size=22,
            render_own_label=True,
            visible={
                'add': 'edit',
            },
        )
    ),

    ExtStringField(
        "OtherParticipantReference",
        mode="rw",
        read_permission=View,
        write_permission=ModifyPortalContent,
        widget=StringWidget(
            label=_("Other Participant Ref"),
            maxlength=12,
            size=12,
            render_own_label=True,
            visible={
                'add': 'edit',
            },
        )
    ),

    ExtStringField(
        "ParticipantInitials",
        mode="rw",
        required=1,
        read_permission=View,
        write_permission=ModifyPortalContent,
        widget=StringWidget(
            label=_("Participant Initials"),
            maxlength=3,
            size=2,
            render_own_label=True,
            visible={
                'add': 'edit',
            },
        )
    ),

    ExtStringField(
        "Gender",
        mode="rw",
        required=1,
        read_permission=View,
        write_permission=ModifyPortalContent,
        vocabulary=GENDERS,
        widget=SelectionWidget(
            format="radio",
            label=_("Gender"),
            render_own_label=True,
            visible={
                'add': 'edit',
            },
        )
    ),

    ExtStringField(
        "Visit",
        mode="rw",
        required=1,
        read_permission=View,
        write_permission=ModifyPortalContent,
        widget=StringWidget(
            label=_("Visit Number"),
            maxlength=4,
            size=4,
            render_own_label=True,
            visible={
                'add': 'edit',
            },
        )
    ),

    ExtBooleanField(
        "Fasting",
        mode="rw",
        required=0,
        read_permission=View,
        write_permission=ModifyPortalContent,
        default=False,
        widget=BooleanWidget(
            format="radio",
            label=_("Fasting"),
            render_own_label=True,
            visible={
                'add': 'edit',
            },
        ),
    ),

    ExtDateTimeField(
        'DateOfBirth',
        mode="rw",
        required=1,
        read_permission=View,
        write_permission=ModifyPortalContent,
        widget=DateTimeWidget(
            label=_('Date of Birth'),
            datepicker_nofuture=1,
            show_time=False,
            render_own_label=True,
            visible={
                'add': 'edit',
            },
        ),
    ),

    ExtStringField(
        "Volume",
        mode="rw",
        required=1,
        read_permission=View,
        write_permission=ModifyPortalContent,
        widget=StringWidget(
            label=_("Estimated Sample Volume"),
            maxlength=8,
            size=8,
            render_own_label=True,
            visible={
                'add': 'edit',
            },
        )
    ),

    ExtTextField(
        "OtherInformation",
        mode="rw",
        read_permission=View,
        write_permission=ModifyPortalContent,
        default_content_type="text/plain",
        allowable_content_types=("text/plain",),
        default_output_type="text/plain",
        widget=TextAreaWidget(
            label=_("Other relevant clinical information"),
            render_own_label=True,
            visible={
                'add': 'edit',
            },
        ),
    ),

    ExtReferenceField(
        "Courier",
        required=0,
        allowed_types='Courier',
        relationship='AnalysisRequestCourier',
        mode="rw",
        read_permission=View,
        write_permission=ModifyPortalContent,
        widget=ReferenceWidget(
            label=_("Courier"),
            description=_("The person who delivered the sample"),
            render_own_label=True,
            visible={
                'view': 'visible',
                'edit': 'visible',
                'add': 'invisible',
                'header_table': 'visible',
                'secondary':    'disabled',
                'sample_registered': {'view': 'invisible', 'edit': 'invisible'},
                'to_be_sampled':     {'view': 'invisible', 'edit': 'invisible'},
                'scheduled_sampling':{'view': 'invisible', 'edit': 'invisible'},
                'sampled':           {'view': 'invisible', 'edit': 'invisible'},
                'to_be_preserved':   {'view': 'invisible', 'edit': 'invisible'},
                'sample_ordered':    {'view': 'visible', 'edit': 'visible'},
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
        ),
    ),

    # This Analysis Request is only for internal use?
    # This field is useful when we create Partitions (AR-like), so we don't
    # want the client to see Analysis Requests / Samples that are meant to
    # be used in the lab.
    ExtBooleanField(
        "InternalUse",
        mode="rw",
        required=0,
        default=False,
        read_permission=View,
        write_permission=ModifyPortalContent,
        widget=BooleanWidget(
            format="radio",
            label=_("Internal use"),
            render_own_label=True,
            visible={
                'add': 'invisible',
                'edit': 'invisible',
                'secondary': 'invisible',
            },
        ),
    ),
    ExtReferenceField(
        "PrimarySample",
        required=0,
        allowed_types=('Sample',),
        relationship='AnalysisRequestPrimarySample',
        mode="rw",
        read_permission=View,
        write_permission=ModifyPortalContent,
        widget=ReferenceWidget(
            label=_("Primary Sample"),
            description=_("The sample this is originated from"),
            size=20,
            render_own_label=True,
            visible=False,
            catalog_name='bika_catalog',
            base_query={'review_state': 'active'},
            showOn=False,
        ),
    ),
    ExtReferenceField(
        'PrimaryAnalysisRequest',
        allowed_types=('AnalysisRequest',),
        relationship='AnalysisRequestPrimaryAnalysisRequest',
        referenceClass=HoldingReference,
        mode="rw",
        read_permission=View,
        write_permission=ModifyPortalContent,
        widget=ReferenceWidget(
            visible=False,
        ),
    ),
    ExtBooleanField(
        "PanicEmailAlertSent",
        default=False,
        widget=BooleanWidget(
            visible=False,
        ),
    ),
    # This field allows to store the assay date manually
    ExtDateTimeField(
        'AssayDate',
        widget=DateTimeWidget(
            label=_('Assay Date'),
            datepicker_nofuture=1,
            show_time=True,
            render_own_label=True,
            visible={
                'add': 'invisible',
                'header_table': 'visible',
            }
        ),
    ),
]

class AnalysisRequestSchemaExtender(object):
    adapts(IAnalysisRequest)
    implements(IOrderableSchemaExtender)

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        return schematas

    def getFields(self):
        return fields


class AnalysisRequestSchemaModifier(object):
    adapts(IAnalysisRequest)
    implements(ISchemaModifier)

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        schema['ClientSampleID'].widget.label = _("Client Sample ID "
                                                  "(if available)")
        schema['Priority'].vocabulary = PRIORITIES
        schema['DateSampled'].widget.label = _("Date Time Sampled")
        schema['ResultsRange'].subfields += ('minpanic', 'maxpanic',
                                             'calculation')
        schema['DefaultContainerType'].widget.visible = {"add": "edit"}
        schema['DefaultContainerType'].widget.label = _("Container Type")
        schema['DefaultContainerType'].widget.description = ""
        schema['DefaultContainerType'].required = 1

        # Fields to always be hided
        hide = ["Batch",
                "CCContact",
                "CCEmails",
                "ClientOrderNumber",
                "ClientReference",
                "Composite",
                "EnvironmentalConditions",
                "InvoiceExclude",
                "Profiles",
                "PublicationSpecification",
                "SamplePoint",
                "SampleCondition",
                "Sampler",
                "SamplingDate",
                "SamplingRound",
                "SamplingDeviation",
                "ScheduledSamplingSampler",
                "StorageLocation",
                "SubGroup", ]

        for field in hide:
            self.hide(schema[field])
        return schema

    def hide(self, schema_field):
        if not schema_field:
            return
        if not schema_field.widget:
            return
        schema_field.widget.visible = False
