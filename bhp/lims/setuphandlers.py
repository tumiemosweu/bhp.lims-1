# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Botswana Harvard Partnership (BHP)

import time

import transaction
from BTrees.OOBTree import OOBTree
from Products.CMFPlone.utils import _createObjectByType
from Products.DCWorkflow.Guard import Guard
from bhp.lims import api
from bhp.lims import bhpMessageFactory as _
from bhp.lims import logger
from bhp.lims.config import GRADES_KEYS
from bhp.lims.specscalculations import get_xls_specifications
from bika.lims.browser.analysisrequest.add2 import AR_CONFIGURATION_STORAGE
from bika.lims.catalog.analysis_catalog import CATALOG_ANALYSIS_LISTING
from bika.lims.catalog.analysisrequest_catalog import \
    CATALOG_ANALYSIS_REQUEST_LISTING
from bika.lims.catalog.catalog_utilities import addZCTextIndex
from bika.lims.idserver import renameAfterCreation
from bika.lims.interfaces import INumberGenerator
from bika.lims.utils import tmpID
from bika.lims.workflow import getTransitionDate
from zope.annotation.interfaces import IAnnotations
from zope.component import getUtility

# Number of objects before commit transaction
TRANSACTION_THERESHOLD = 1000

PROFILE_STEPS = [
    # List of profile steps to be reimported
    "jsregistry",
]

CONTROL_PANELS = [
    # List of items to be added in control panel, inside Setup and nav portlet
    {
        "id": "barcodeprinters",
        "type": "BarcodePrinters",
        "title": "Barcode Printers",
        "description": "",
        "insert-after": "*"
    },
    {
        "id": "referrallabs",
        "type": "ReferralLabs",
        "title": "Referral Laboratories",
        "description": "",
        "insert-after": "*"
    }
]

NEW_CONTENT_TYPES = [
    # Tuples of (id, folder_id)
    # If folder_id is None, assume folder_id is portal
    ("couriers", "bika_setup"),
]

CATALOGS_BY_TYPE = [
    # Tuples of (type, [catalog])
    ("BarcodePrinter", ["bika_setup_catalog"]),
    ("Courier", ["bika_setup_catalog"]),
    ("ReferralLab", ["bika_setup_catalog"]),
]

INDEXES = [
    # Tuples of (catalog, index_name, index_type)
    ("bika_analysis_catalog", "getAncestorsUIDs", "KeywordIndex"),
    (CATALOG_ANALYSIS_REQUEST_LISTING, "getParticipantID", "FieldIndex"),
]

COLUMNS = [
    # Tuples of (catalog, column name)
    (CATALOG_ANALYSIS_REQUEST_LISTING, "getParticipantID"),
    (CATALOG_ANALYSIS_REQUEST_LISTING, "getVisit"),
]

ID_FORMATTING = [
    # An array of dicts. Each dict represents an ID formatting configuration
    {"portal_type": "AnalysisRequest",
     "form": "{studyId}{sampleType}{alpha:3a2d}",
     "prefix": "analysisrequest",
     "sequence_type": "generated",
     "counter_type": "",
     "split_length": 2,
    },
    {"portal_type": "AnalysisRequestPartition",
     "form": "{studyId}{sampleType}{parent_alpha}{partition_count}",
     "prefix": "analysisrequest_partition",
     "sequence_type": "generated",
     "counter_type": "",
     "split_length": 3,
     },
]

IDS_TO_FLUSH = (
    # List of IDFormatting prefixes used for IDs storage by NumberGenerator.
    # The upgrade step will flush all IDs starting with this prefix
    # Look at http://localhost:8080/senaite/ng
)

NEW_ATTACHMENT_TYPES = [
    # List of names with Attachment Types to be created
    "Delivery",
    "Requisition",
]

ADD_AR_FIELDS_TO_HIDE = [
    # List of field names to not display in AR Add form
    "Sample",
    "RejectionReasons",
    "Specification",
    "InternalUse",
    "Container",
    "Preservation",
    "PrimaryAnalysisRequest",
]

ADD_AR_FIELDS_SORTED = [
    # List of AR field names, sorted in order for AR Add form
    'Client',
    'Contact',
    'ParticipantID',
    'OtherParticipantReference',
    'ParticipantInitials',
    'Gender',
    'Visit',
    'VisitCode',
    'DayWeekNumber',
    'DateOfBirth',
    'Fasting',
    'ClientSampleID',
    'DateSampled',
    'SampleType',
    'Volume',
    'DefaultContainerType',
    'Template',
    'OtherInformation',
    '_ARAttachment',
    'Priority',
    'Remarks',
]

WORKFLOWS_TO_UPDATE = {
    "bika_ar_workflow": {
        "permissions": (),
        "states": {
            # Clinic has submitted the Sample (Add form)
            "sample_ordered": {
                "title": "Ordered",
                "description": "Sample ordered",
                "transitions": ("send_to_lab", "cancel"),
                "permissions_copy_from": "sample_due",
            },

            # Clinic has sent the sample to lab
            "sample_shipped": {
                "title": "Shipped",
                "description": "Sample shipped",
                "transitions": ("deliver", "cancel"),
                "permissions_copy_from": "sample_due",
            },

            # Reception has received the sample
            "sample_at_reception": {
                "title": "At reception",
                "description": "Sample at reception",
                "transitions": ("send_to_pot", "process", "reject", "detach", "store",),
                "permissions_copy_from": "sample_due",
            },

            # Reception has sent the sample to points of testing
            "sample_due": {
                "title": "Sent to point of testing",
                "description": "Sample sent to point of testing",
                "transitions": ("detach", "store"),
                "preserve_transitions": True,
            },

            # Point of testing has received the sample
            "sample_received": {
                "title": "At point of testing",
                "description": "Sample at point of testing",
                "transitions": ("detach", "store"),
                "preserve_transitions": True,
            },
        },
        "transitions": {
            # Clinic submits the sample (Add form)
            "no_sampling_workflow": {
                "new_state": "sample_ordered",
            },

            # Clinic sends the sample to the laboratory
            "send_to_lab": {
                "title": "Send to lab",
                "new_state": "sample_shipped",
                "guard": {
                    "guard_permissions": "",
                    "guard_roles": "",
                    "guard_expr": "python:here.guard_send_to_lab()",
                }
            },

            # Reception receives the sample at the lab
            "deliver": {
                "title": "Receive at reception",
                "new_state": "sample_at_reception",
                "guard": {
                    "guard_permissions": "",
                    "guard_roles": "",
                    "guard_expr": "python:here.guard_deliver()",
                }
            },

            # Reception processes the sample (partitioning)
            "process": {
                "title": "Process",
                "new_state": "sample_at_reception",
                "guard": {
                    "guard_permissions": "",
                    "guard_roles": "",
                    "guard_expr": "python:here.guard_process()",
                }
            },

            # Reception sends the sample to point of testing
            "send_to_pot": {
                "title": "Send to point of testing",
                "new_state": "sample_due",
                "guard": {
                    "guard_permissions": "",
                    "guard_roles": "",
                    "guard_expr": "python:here.guard_send_to_pot()",
                }
            },

            # Point of testing receives the sample
            "receive": {
                "title": "Receive at point of testing",
                "new_state": "sample_received",
                "guard": {
                    "guard_permissions": "BIKA: Receive Sample",
                    "guard_roles": "",
                    "guard_expr": 'python:here.guard_receive_at_pot()'
                }
            },

        }
    }
}

ROLE_MAPPINGS = [
    # List of tuples: (wf_id, query, catalog_name)
    ("bika_ar_workflow",
     dict(portal_type="AnalysisRequest",
          review_state=[
              "sample_ordered",
              "sample_shipped",
              "sample_at_reception",
              "sample_due",
              "sample_received",
              "stored"]),
     CATALOG_ANALYSIS_REQUEST_LISTING)
]

OBJECTS_TO_REINDEX = [
    # List of tuples (catalog_name, query)
]

# BHP-specific
# List of Zebra printers (BarcodePrinter content type) to create by default
PRINTERS = {
    "Zebra Printer Template 1": {
        "FileName": "lims-${id}.zpl",
        "PrinterPath": "/tmp/",
        "Template":
        """^XA^PR4
^FO315,15^A0N,20,15^FD${ClientID} ${TaxNumber} ${SampleType.Prefix}^FS
^FO315,34^BY1^BCN,50,N,N,N,A
^FD${id}^FS
^FO315,92^A0N,20,15^FD${id} ${Template.title}^FS
^FO315,112^A0N,20,15^FD${ParticipantID} ${ParticipantInitials}^FS
^FO315,132^A0N,20,15^FDDOB: ${DateOfBirth|to_date} ${Gender}^FS
^FO315,152^A0N,20,15^FD${DateSampled|to_long_date}^FS
^XZ"""
    },
}


def setup_handler(context):
    """BHP setup handler
    """

    if context.readDataFile('bhp.lims.txt') is None:
        return

    logger.info("BHP setup handler [BEGIN]")

    portal = context.getSite()

    # Setup Catalogs
    setup_catalogs(portal)

    # Run installers
    setup_laboratory(portal)

    # Add new content types
    reindex_new_content_types(portal)

    # Apply ID format to content types
    setup_id_formatting(portal)

    # Flush IDs from NumberGenerator
    flush_ids(portal)

    # Setup custom workflow(s)
    setup_workflows(portal)

    # Update role mappings
    update_role_mappings(portal)

    # Hide unused AR Fields
    hide_ar_add_fields(portal)

    # Sort AR fields (AR Add)
    sort_ar_add_fields(portal)

    # Setup Attachment Types (requisition + delivery)
    setup_attachment_types(portal)

    # Update priorities to Urgent, Routine, STAT
    update_priorities(portal)

    # update analysis services (Replace % by PCT in Analysis Keywords)
    update_services_percentage_keyword(portal)

    # Import specifications from bhp/lims/resources/results_ranges.xlsx
    import_specifications(portal)

    # Assign the specifications to ARs with missing specs
    fix_analysis_requests_without_specifications(portal)

    # Remove "Results Ranges" calculation from analyses and service
    sanitize_ranges_calculation_from_analyses(portal)

    # Fix analyses from Storage category that have instruments assigned
    fix_analyses_storage_instrument(portal)

    # Set default Assay Date values to old Analysis Requests
    fix_analysis_requests_assay_date(portal)

    # Setup Controlpanels
    setup_control_panels(portal)

    # Setup printer stickers
    setup_printer_stickers(portal)

    # Reimport additional steps from profile
    import_profile_steps(portal)

    # Disable auto-partitioning
    disable_autopartitioning(portal)

    # Reindex objects
    reindex_objects(portal)

    # Set the date the Sample was received at the lab, not at point of testing
    # https://github.com/bhp-lims/bhp.lims/issues/233
    fix_i233(portal)

    logger.info("BHP setup handler [DONE]")


def setup_printer_stickers(portal):
    """Setup printers and stickers templates
    """
    logger.info("Setting up printers and stickers ...")

    def create_printer(folder, name, values):
        query = dict(portal_type="BarcodePrinter", Title=name)
        brains = api.search(query, "bika_setup_catalog")
        if brains:
            printer = api.get_object(brains[0])
            printer.FileName = values["FileName"]
            printer.PrinterPath = values["PrinterPath"]
            printer.Template = values["Template"]
            return printer

        # Create a new Barcode Printer
        obj = _createObjectByType("BarcodePrinter", folder, tmpID())
        obj.edit(title=name,
                 FileName=values["FileName"],
                 PrinterPath=values["PrinterPath"],
                 Template=values["Template"])
        obj.unmarkCreationFlag()
        renameAfterCreation(obj)

    printers = portal.bika_setup.barcodeprinters
    for printer_name, printer_values in PRINTERS.items():
        create_printer(printers, printer_name, printer_values)
    logger.info("Setting up printers and stickers [DONE]")


def setup_laboratory(portal):
    """Setup Laboratory
    """
    logger.info("Setting up Laboratory ...")
    lab = portal.bika_setup.laboratory
    lab.edit(title=_('BHP'))
    lab.reindexObject()

    # Set autoprinting of stickers on register
    portal.bika_setup.setAutoPrintStickers('register')

    # Unselect ShowPartitions from setup to hide partitions to Clients
    # https://github.com/senaite/senaite.core/pull/1392
    portal.bika_setup.setShowPartitions(False)

    logger.info("Setting up Laboratory [DONE]")


def reindex_new_content_types(portal):
    """Setup new content types"""
    logger.info("Reindex new content types ...")

    def reindex_content_type(object_id, folder):
        logger.info("Reindexing {}".format(object_id))
        obj = folder[object_id]
        obj.unmarkCreationFlag()
        obj.reindexObject()

    # Index objects - Importing through GenericSetup doesn't
    for obj_id, folder_id in NEW_CONTENT_TYPES:
        content_type_folder = folder_id and portal[folder_id] or portal
        reindex_content_type(obj_id, content_type_folder)

    logger.info("Reindex new content types [DONE]")


def setup_id_formatting(portal, format_definition=None):
    """Setup default ID formatting
    """
    if not format_definition:
        logger.info("Setting up ID formatting ...")
        for formatting in ID_FORMATTING:
            setup_id_formatting(portal, format_definition=formatting)
        logger.info("Setting up ID formatting [DONE]")
        return

    bs = portal.bika_setup
    p_type = format_definition.get("portal_type", None)
    if not p_type:
        return

    form = format_definition.get("form", "")
    if not form:
        logger.info("Param 'form' for portal type {} not set [SKIP")
        return

    logger.info("Applying format '{}' for {}".format(form, p_type))
    ids = list()
    for record in bs.getIDFormatting():
        if record.get('portal_type', '') == p_type:
            continue
        ids.append(record)
    ids.append(format_definition)
    bs.setIDFormatting(ids)


def flush_ids(portal):
    def to_flush(key):
        for id in IDS_TO_FLUSH:
            if key.startswith(id):
                return True
        return False

    number_generator = getUtility(INumberGenerator)
    keys = filter(lambda key: to_flush(key), number_generator.keys())
    for key in keys:
        logger.info("Flush ID {}".format(key))
        del number_generator.storage[key]


def get_manage_add_storage(portal):
    bika_setup = portal.bika_setup
    annotation = IAnnotations(bika_setup)
    storage = annotation.get(AR_CONFIGURATION_STORAGE)
    if storage is None:
        annotation[AR_CONFIGURATION_STORAGE] = OOBTree()
    return annotation[AR_CONFIGURATION_STORAGE]


def update_manage_add_storage(portal, storage):
    bika_setup = portal.bika_setup
    annotation = IAnnotations(bika_setup)
    annotation[AR_CONFIGURATION_STORAGE] = storage


def flush_manage_add_storage(portal):
    bika_setup = portal.bika_setup
    annotation = IAnnotations(bika_setup)
    if annotation[AR_CONFIGURATION_STORAGE]:
        del annotation[AR_CONFIGURATION_STORAGE]


def hide_ar_add_fields(portal):
    """Hides unused fields from AR Add Form
    """
    logger.info("Hiding default fields from AR Add ...")
    storage = get_manage_add_storage(portal)
    visibility = storage.get('visibility', {}).copy()
    ordered = storage.get('order', [])
    fields = list(set(visibility.keys() + ADD_AR_FIELDS_TO_HIDE + ordered))
    for field_name in fields:
        visibility[field_name] = field_name not in ADD_AR_FIELDS_TO_HIDE
    storage.update({"visibility": visibility})
    update_manage_add_storage(portal, storage)
    logger.info("Hiding default fields from AR Add [DONE]")


def sort_ar_add_fields(portal):
    """Sort AR fields from AR Add Form
    """
    logger.info("Sorting fields from AR Add ...")
    storage = get_manage_add_storage(portal)
    storage.update({"order": ADD_AR_FIELDS_SORTED})
    update_manage_add_storage(portal, storage)
    logger.info("Sorting fields from AR Add [DONE]")


def setup_workflows(portal):
    """Setup workflows
    """
    logger.info("Setting up workflows ...")
    for wf_id, settings in WORKFLOWS_TO_UPDATE.items():
        update_workflow(wf_id, settings)
    logger.info("Setting up workflows [DONE]")


def update_workflow(workflow_id, settings):
    logger.info("Updating workflow '{}' ...".format(workflow_id))
    wf_tool = api.get_tool("portal_workflow")
    workflow = wf_tool.getWorkflowById(workflow_id)
    if not workflow:
        logger.warn("Workflow '{}' not found [SKIP]".format(workflow_id))
    states = settings.get("states", {})
    for state_id, values in states.items():
        update_workflow_state(workflow, state_id, values)

    transitions = settings.get("transitions", {})
    for transition_id, values in transitions.items():
        update_workflow_transition(workflow, transition_id, values)


def update_workflow_state(workflow, status_id, settings):
    logger.info("Updating workflow '{}', status: '{}' ..."
                .format(workflow.id, status_id))

    # Create the status (if does not exist yet)
    new_status = workflow.states.get(status_id)
    if not new_status:
        workflow.states.addState(status_id)
        new_status = workflow.states.get(status_id)

    # Set basic info (title, description, etc.)
    new_status.title = settings.get("title", new_status.title)
    new_status.description = settings.get("description", new_status.description)

    # Set transitions
    trans = settings.get("transitions", ())
    if settings.get("preserve_transitions", False):
        trans = tuple(set(new_status.transitions+trans))
    new_status.transitions = trans

    # Set permissions
    update_workflow_state_permissions(workflow, new_status, settings)


def update_workflow_state_permissions(workflow, status, settings):
    # Copy permissions from another state?
    permissions_copy_from = settings.get("permissions_copy_from", None)
    if permissions_copy_from:
        logger.info("Copying permissions from '{}' to '{}' ..."
                    .format(permissions_copy_from, status.id))
        copy_from_state = workflow.states.get(permissions_copy_from)
        if not copy_from_state:
            logger.info("State '{}' not found [SKIP]".format(copy_from_state))
        else:
            for perm_id in copy_from_state.permissions:
                perm_info = copy_from_state.getPermissionInfo(perm_id)
                acquired = perm_info.get("acquired", 1)
                roles = perm_info.get("roles", acquired and [] or ())
                logger.info("Setting permission '{}' (acquired={}): '{}'"
                            .format(perm_id, repr(acquired), ', '.join(roles)))
                status.setPermission(perm_id, acquired, roles)

    # Override permissions
    logger.info("Overriding permissions for '{}' ...".format(status.id))
    state_permissions = settings.get('permissions', {})
    if not state_permissions:
        logger.info("No permissions set for '{}' [SKIP]".format(status.id))
        return
    for permission_id, roles in state_permissions.items():
        state_roles = roles and roles or ()
        if isinstance(state_roles, tuple):
            acq = 0
        else:
            acq = 1
        logger.info("Setting permission '{}' (acquired={}): '{}'"
                    .format(permission_id, repr(acq), ', '.join(state_roles)))
        status.setPermission(permission_id, acq, state_roles)


def update_workflow_transition(workflow, transition_id, settings):
    logger.info("Updating workflow '{}', transition: '{}'"
                .format(workflow.id, transition_id))
    if transition_id not in workflow.transitions:
        workflow.transitions.addTransition(transition_id)
    transition = workflow.transitions.get(transition_id)
    transition.setProperties(
        title=settings.get("title"),
        new_state_id=settings.get("new_state"),
        after_script_name=settings.get("after_script", ""),
        actbox_name=settings.get("action", settings.get("title"))
    )
    guard = transition.guard or Guard()
    guard_props = {"guard_permissions": "",
                   "guard_roles": "",
                   "guard_expr": ""}
    guard_props = settings.get("guard", guard_props)
    guard.changeFromProperties(guard_props)
    transition.guard = guard


def update_role_mappings(portal):
    logger.info("Updating role mappings ...")
    processed = dict()
    for rm_query in ROLE_MAPPINGS:
        wf_tool = api.get_tool("portal_workflow")
        wf_id = rm_query[0]
        workflow = wf_tool.getWorkflowById(wf_id)

        query = rm_query[1].copy()
        exclude_states = []
        if 'not_review_state' in query:
            exclude_states = query.get('not_review_state', [])
            del query['not_review_state']

        brains = api.search(query, rm_query[2])
        total = len(brains)
        for num, brain in enumerate(brains):
            if num % 100 == 0:
                logger.info("Updating role mappings '{0}': {1}/{2}"
                            .format(wf_id, num, total))
            if api.get_uid(brain) in processed.get(wf_id, []):
                # Already processed, skip
                continue

            if api.get_workflow_status_of(brain) in exclude_states:
                # We explicitely want to exclude objs in these states
                continue

            workflow.updateRoleMappingsFor(api.get_object(brain))
            if wf_id not in processed:
                processed[wf_id] = []
            processed[wf_id].append(api.get_uid(brain))
    logger.info("Updating role mappings [DONE]")


def update_priorities(portal):
    """Reset the priorities of created ARs to those defined for BHP
    1: Urgent, 3: Routine, 5: STAT
    """
    logger.info("Restoring Priorities ...")
    query = dict(portal_type='AnalysisRequest')
    brains = api.search(query, CATALOG_ANALYSIS_REQUEST_LISTING)
    for brain in brains:
        obj = api.get_object(brain)
        if obj.getPriority() == '2':
            # High --> Urgent (1)
            obj.setPriority(1)
            obj.reindexObject()
        elif obj.getPriority() == '4':
            # Low --> STAT
            obj.setPriority(5)
            obj.reindexObject()
    logger.info("Restoring Priorities [DONE]")


def update_services_percentage_keyword(portal):
    """Replace "%" character in Analysis Service keywords by "_PCT"
    """
    logger.info("Updating services ...")
    for service in portal.bika_setup.bika_analysisservices.values():
        keyword = service.Schema().getField('Keyword').get(service)
        if '%' in keyword:
            keyword = keyword.replace('%', '_PCT')
            logger.info("Replaced Analysis Keyword: {}".format(keyword))
            service.setKeyword(keyword)
            service.reindexObject()
    logger.info("Updating services [DONE]")


def setup_attachment_types(portal):
    """Creates two attachment types. One for requisition and another one for
    the checklist delivery report
    """
    logger.info("Creating custom Attachment Types ...")
    new_attachment_types = list(NEW_ATTACHMENT_TYPES)
    folder = portal.bika_setup.bika_attachmenttypes
    for attachment in folder.values():
        if attachment.Title() in new_attachment_types:
            new_attachment_types.remove(attachment.Title())

    for new_attachment in new_attachment_types:
        obj = _createObjectByType("AttachmentType", folder, tmpID())
        obj.edit(title=new_attachment,
                 description="Attachment type for {} files".format(new_attachment))
        obj.unmarkCreationFlag()
        renameAfterCreation(obj)

    logger.info("Assign Attachment Types to requisition and rejection")
    new_attachment_types = dict.fromkeys(NEW_ATTACHMENT_TYPES)
    for attachment in folder.values():
        for att_type in new_attachment_types.keys():
            if attachment.Title() == att_type:
                new_attachment_types[att_type] = attachment
                break

    query = dict(portal_type='AnalysisRequest')
    brains = api.search(query, CATALOG_ANALYSIS_REQUEST_LISTING)
    for brain in brains:
        obj = api.get_object(brain)
        attachments = obj.getAttachment()
        for attachment in attachments:
            if attachment.getAttachmentType():
                continue
            for key, val in new_attachment_types.items():
                if key.lower() in attachment.getAttachmentFile().filename:
                    attachment.setAttachmentType(val)
                    attachment.setReportOption('i') # Ignore in report
                    break
    logger.info("Creating custom Attachment Types [DONE]")


def import_specifications(portal):
    """Creates (or updates) dynamic specifications from
    resources/results_ranges.xlsx
    """
    logger.info("Importing specifications ...")

    query = dict(portal_type='SampleType')
    brains = api.search(query, 'bika_setup_catalog')
    sample_types = map(lambda brain: api.get_object(brain), brains)
    for sample_type in sample_types:
        import_specifications_for_sample_type(portal, sample_type)

    apply_specifications_to_all_sampletypes(portal)

    logger.info("Importing specifications [DONE]")


def import_specifications_for_sample_type(portal, sample_type):
    logger.info("Importing specs for {}".format(sample_type.Title()))

    def get_bs_object(xlsx_row, xlsx_keyword, portal_type, criteria):
        text_value = xlsx_row.get(xlsx_keyword, None)
        if not text_value:
            logger.warn("Value not set for keyword {}".format(xlsx_keyword))
            return None

        query = {"portal_type": portal_type, criteria: text_value}
        brain = api.search(query, 'bika_setup_catalog')
        if not brain:
            logger.warn("No objects found for type {} and {} '{}'"
                        .format(portal_type, criteria, text_value))
            return None
        if len(brain) > 1:
            logger.warn("More than one object found for type {} and {} '{}'"
                        .format(portal_type, criteria, text_value))
            return None

        return api.get_object(brain[0])

    raw_specifications = get_xls_specifications()
    for spec in raw_specifications:

        # Valid Analysis Service?
        service = get_bs_object(spec, "keyword", "AnalysisService",
                                "getKeyword")
        if not service:
            continue

        # The calculation exists?
        calc_title = "Ranges calculation"
        query = dict(calculation=calc_title)
        calc = get_bs_object(query, "calculation", "Calculation", "title")
        if not calc:
            # Create a new one
            folder = portal.bika_setup.bika_calculations
            _id = folder.invokeFactory("Calculation", id=tmpID())
            calc = folder[_id]
            calc.edit(title=calc_title,
                      PythonImports=[{"module": "bhp.lims.specscalculations",
                                      "function": "get_specification_for"}],
                      Formula="get_specification_for($spec)")
            calc.unmarkCreationFlag()
            renameAfterCreation(calc)

        # Existing AnalysisSpec?
        specs_title = "{} - calculated".format(sample_type.Title())
        query = dict(portal_type='AnalysisSpec', title=specs_title)
        aspec = api.search(query, 'bika_setup_catalog')
        if not aspec:
            # Create the new AnalysisSpecs object!
            folder = portal.bika_setup.bika_analysisspecs
            _id = folder.invokeFactory('AnalysisSpec', id=tmpID())
            aspec = folder[_id]
            aspec.edit(title=specs_title)
            aspec.unmarkCreationFlag()
            renameAfterCreation(aspec)
        elif len(aspec) > 1:
            logger.warn("More than one Analysis Specification found for {}"
                        .format(specs_title))
            continue
        else:
            aspec = api.get_object(aspec[0])
        aspec.setSampleType(sample_type)

        # Set the analysis keyword and bind it to the calculation to use
        keyword = service.getKeyword()
        specs_dict = {
            'keyword': keyword,
            'min_operator': 'geq',
            'min': '0',
            'max_operator': 'lt',
            'max': '0',
            'minpanic': '',
            'maxpanic': '',
            'warn_min': '',
            'warn_max': '',
            'hidemin': '',
            'hidemax': '',
            'rangecomments': '',
            'calculation': api.get_uid(calc),
        }
        grades_dict = {grade: "" for grade in GRADES_KEYS}
        specs_dict.update(grades_dict)
        ranges = api.get_field_value(aspec, 'ResultsRange', [{}])
        ranges = filter(lambda val: val.get('keyword') != keyword, ranges)
        ranges.append(specs_dict)
        aspec.setResultsRange(ranges)


def apply_specifications_to_all_sampletypes(portal):
    logger.info("Applying specs to all sample types ...")

    def set_xlsx_specs(senaite_spec):
        logger.info("Applying specs to {}".format(senaite_spec.Title()))
        query = dict(portal_type="Calculation", title="Ranges calculation")
        calc = api.search(query, "bika_setup_catalog")
        if len(calc) == 0 or len(calc) > 1:
            logger.info("No calculation found [SKIP]")
            return
        calc_uid = api.get_uid(calc[0])
        keywords = list()
        raw_specifications = get_xls_specifications()
        for spec in raw_specifications:
            keyword = spec.get("keyword")
            if keyword not in keywords:
                query = dict(portal_type="AnalysisService", getKeyword=keyword)
                brains = api.search(query, "bika_setup_catalog")
                if len(brains) == 0 or len(brains) > 1:
                    logger.info("No service found for {} [SKIP]"
                                .format(keyword))
                    continue
                keywords.append(keyword)

            specs_dict = {
                'keyword': keyword,
                'min_operator': 'geq',
                'min': '0',
                'max_operator': 'lt',
                'max': '0',
                'minpanic': '',
                'maxpanic': '',
                'warn_min': '',
                'warn_max': '',
                'hidemin': '',
                'hidemax': '',
                'rangecomments': '',
                'calculation': calc_uid,
            }
            grades_dict = {grade: "" for grade in GRADES_KEYS}
            specs_dict.update(grades_dict)
            ranges = api.get_field_value(senaite_spec, 'ResultsRange', [{}])
            ranges = filter(lambda val: val.get('keyword') != keyword, ranges)
            ranges.append(specs_dict)
            senaite_spec.setResultsRange(ranges)

    # Existing AnalysisSpec?
    query = dict(portal_type='AnalysisSpec')
    senaite_specs = api.search(query, 'bika_setup_catalog')
    for senaite_spec in senaite_specs:
        senaite_spec = api.get_object(senaite_spec)
        if not senaite_spec.Title().endswith("calculated"):
            continue
        set_xlsx_specs(senaite_spec)
    logger.info("Applying specs to all sample types [DONE]")


def fix_analysis_requests_without_specifications(portal):
    """Walks through all Analysis Requests not yet published and assigns the
    suitable specification
    """
    logger.info("Updating Specifications for Analysis Requests")
    query = dict(portal_type="AnalysisRequest")
    brains = api.search(query, CATALOG_ANALYSIS_REQUEST_LISTING)
    for brain in brains:
        if brain.review_state in ['published', 'rejected', 'invalid']:
            continue
        ar = api.get_object(brain)
        if ar.getSpecification():
            continue

        sample_type = ar.getSampleType().Title()
        specs_title = "{} - calculated".format(sample_type)
        query = dict(portal_type="AnalysisSpec", title=specs_title)
        specs = api.search(query, 'bika_setup_catalog')
        if specs:
            ar.setSpecification(api.get_object(specs[0]))
    logger.info("Updating Specifications for Analysis Requests [DONE]")


def sanitize_ranges_calculation_from_analyses(portal):
    """Walks through all Analyses not yet verified and remove the calculation
    if is Ranges Calculation set
    """
    logger.info("Sanitizing 'Ranges Calculation' from analyses")
    query = dict(portal_type="Calculation", title="Ranges calculation")
    calc = api.search(query, "bika_setup_catalog")
    if not calc:
        logger.warn("Calculation 'Ranges calculation' not found! [SKIP]")
        return
    calc = api.get_object(calc[0])
    calc_uid = api.get_uid(calc)

    # Cleanup analysis services first
    query = dict(portal_type="AnalysisService", getCalculationUID=calc_uid)
    brains = api.search(query, "bika_setup_catalog")
    for brain in brains:
        service = api.get_object(brain)
        service.setCalculation(None)
        service.reindexObject()

    # Cleanup analyses
    query = dict()
    brains = api.search(query, CATALOG_ANALYSIS_LISTING)
    for brain in brains:
        if brain.getCalculationUID != calc_uid:
            continue
        analysis = api.get_object(brain)
        analysis.setCalculation(None)
        analysis.reindexObject()
    logger.info("Sanitizing 'Ranges Calculation' from analyses [DONE]")


def fix_analyses_storage_instrument(portal):
    """Walks through all Analyses not yet verified and if they belong to the
    Storage requisition category, remove the instrument assignment
    """
    logger.info("Sanitizing 'Storage instrument' from analyses")
    query = dict(portal_type="AnalysisCategory", title="Storage requisition")
    cat = api.search(query, "bika_setup_catalog")
    if not cat:
        logger.warn("Category 'Storage requisition' not found [SKIP]")
        return

    cat_uid = api.get_uid(cat[0])

    # Cleanup analysis services first
    query = dict(portal_type="AnalysisService", getCategoryUID=cat_uid)
    brains = api.search(query, "bika_setup_catalog")
    for brain in brains:
        service = api.get_object(brain)
        if not service.getInstrument():
            continue
        service.setInstrument(None)
        service.reindexObject()

    # Cleanup analyses
    query = dict(getCategoryUID=cat_uid,)
    brains = api.search(query, CATALOG_ANALYSIS_LISTING)
    for brain in brains:
        if brain.review_state in ['published', 'rejected', 'invalid']:
            continue
        if not brain.getInstrumentUID:
            continue
        analysis = api.get_object(brain)
        analysis.setInstrument(None)
        analysis.reindexObject()
    logger.info("Sanitizing 'Storage instrument' from analyses [DONE]")


def setup_control_panels(portal):
    """Setup Plone control and Senaite management panels
    """
    logger.info("Setup Control panels ...")

    # get the bika_setup object
    bika_setup = api.get_bika_setup()
    cp = api.get_tool("portal_controlpanel")

    def get_action_index(action_id):
        if action_id == "*":
            action = cp.listActions()[-1]
            action_id = action.getId()
        for n, action in enumerate(cp.listActions()):
            if action.getId() == action_id:
                return n
        return -1

    for item in CONTROL_PANELS:
        id = item.get("id")
        type = item.get("type")
        title = item.get("title")
        description = item.get("description")

        panel = bika_setup.get(id, None)
        if panel is None:
            logger.info("Creating Setup Folder '{}' in Setup.".format(id))
            # allow content creation in setup temporary
            portal_types = api.get_tool("portal_types")
            fti = portal_types.getTypeInfo(bika_setup)
            fti.filter_content_types = False
            myfti = portal_types.getTypeInfo(type)
            global_allow = myfti.global_allow
            myfti.global_allow = True
            _ = bika_setup.invokeFactory(type, id, title=title)
            panel = bika_setup[_]
            myfti.global_allow = global_allow
            fti.filter_content_types = True
        else:
            # set some meta data
            panel.setTitle(title)
            panel.setDescription(description)

        # Move configlet action to the right index
        action_index = get_action_index(id)
        ref_index = get_action_index(item["insert-after"])
        if (action_index != -1) and (ref_index != -1):
            actions = cp._cloneActions()
            action = actions.pop(action_index)
            actions.insert(ref_index + 1, action)
            cp._actions = tuple(actions)
            cp._p_changed = 1

        # reindex the object to render it properly in the navigation portlet
        panel.reindexObject()
    logger.info("Setup Control panels [DONE]")


def setup_catalogs(portal):
    """Setup Plone catalogs
    """
    logger.info("Setup Catalogs ...")

    # Setup catalogs by type
    for type_name, catalogs in CATALOGS_BY_TYPE:
        at = api.get_tool("archetype_tool")
        # get the current registered catalogs
        current_catalogs = at.getCatalogsByType(type_name)
        # get the desired catalogs this type should be in
        desired_catalogs = map(api.get_tool, catalogs)
        # check if the catalogs changed for this portal_type
        if set(desired_catalogs).difference(current_catalogs):
            # fetch the brains to reindex
            brains = api.search({"portal_type": type_name})
            # updated the catalogs
            at.setCatalogsByType(type_name, catalogs)
            logger.info("Assign '%s' type to Catalogs %s" %
                        (type_name, catalogs))
            for brain in brains:
                obj = api.get_object(brain)
                logger.info("Reindexing '%s'" % repr(obj))
                obj.reindexObject()

    # Setup catalog indexes
    to_index = []
    for catalog, name, meta_type in INDEXES:
        c = api.get_tool(catalog)
        indexes = c.indexes()
        if name in indexes:
            logger.info("Index '%s' already in Catalog [SKIP]" % name)
            continue

        logger.info("Adding Index '%s' for field '%s' to catalog '%s"
                    % (meta_type, name, catalog))
        if meta_type == "ZCTextIndex":
            addZCTextIndex(c, name)
        else:
            c.addIndex(name, meta_type)
        to_index.append((c, name))
        logger.info("Added Index '%s' for field '%s' to catalog [DONE]"
                    % (meta_type, name))

    for catalog, name in to_index:
        logger.info("Indexing new index '%s' ..." % name)
        catalog.manage_reindexIndex(name)
        logger.info("Indexing new index '%s' [DONE]" % name)

    # Setup catalog metadata columns
    for catalog, name in COLUMNS:
        c = api.get_tool(catalog)
        if name not in c.schema():
            logger.info("Adding Column '%s' to catalog '%s' ..."
                        % (name, catalog))
            c.addColumn(name)
            logger.info("Added Column '%s' to catalog '%s' [DONE]"
                        % (name, catalog))
        else:
            logger.info("Column '%s' already in catalog '%s'  [SKIP]"
                        % (name, catalog))
            continue
    logger.info("Setup Catalogs [DONE]")


def import_profile_steps(portal):
    logger.info("Importing profile steps...")
    setup = portal.portal_setup
    for step in PROFILE_STEPS:
        logger.info("Importing profile step: {}".format(step))
        setup.runImportStepFromProfile('profile-bhp.lims:default', step)
    logger.info("Importing profile steps [DONE]")


def fix_analysis_requests_assay_date(portal):
    logger.info("Updating Assay Date for old Analysis Requests ...")
    query = dict(portal_type="AnalysisRequest",
                 review_state=["published", "to_be_verified", "verified",
                               "invalid"])
    brains = api.search(query, CATALOG_ANALYSIS_REQUEST_LISTING)
    total = len(brains)
    for num, brain in enumerate(brains):
        if num % 100 == 0:
            logger.info("Updating Assay Date for old Analysis Requests: {}/{}"
                        .format(num, total))
        if num % TRANSACTION_THERESHOLD == 0:
            commit_transaction(portal)

        request = api.get_object(brain)
        if not api.get_field_value(request, "AssayDate", None):
            review_states = ["to_be_verified", "published", "verified"]
            analyses = request.getAnalyses(review_state=review_states)
            captures = map(lambda an: an.getResultCaptureDate, analyses)
            captures = sorted(captures)
            if captures:
                api.set_field_value(request, "AssayDate", captures[-1])
                request.reindexObject()
    commit_transaction(portal)
    logger.info("Updating Assay Date for old Analysis Requests [DONE]")


def commit_transaction(portal):
    start = time.time()
    logger.info("Commit transaction ...")
    transaction.commit()
    end = time.time()
    logger.info("Commit transaction ... Took {:.2f}s [DONE]"
                .format(end - start))


def reindex_objects(portal):
    logger.info("Reindexing objects ...")
    def reindex(query, catalog_name, job_num):
        brains = api.search(query, catalog_name)
        total = len(brains)
        for num, brain in enumerate(brains):
            if num % 100 == 0:
                logger.info(
                    "Reindexing objects (job {}): {}/{}"
                    .format(job_num, num, total))
            if num % TRANSACTION_THERESHOLD == 0:
                commit_transaction(portal)
            obj = api.get_object(brain)
            obj.reindexObject()
        commit_transaction(portal)

    count = 1
    steps = len(OBJECTS_TO_REINDEX)
    for catalog_name, query in OBJECTS_TO_REINDEX:
        logger.info("Reindexing objects {} jobs of {}...".format(count, steps))
        reindex(query, catalog_name, count)
        count += 1

    logger.info("Reindexing objects [DONE]")


def disable_autopartitioning(portal):
    logger.info("Disabling auto-partitioning for Templates ...")
    query = dict(portal_type="ARTemplate")
    for template in api.search(query, "portal_catalog"):
        template = api.get_object(template)
        template.setAutoPartition(False)
        template.reindexObject()
    logger.info("Disabling auto-partitioning for Templates [DONE]")


def fix_i233(portal):
    """Set the date the Sample was received at the lab, not at point of testing
    https://github.com/bhp-lims/bhp.lims/issues/233
    """
    logger.info("Reseting Date Received (#233) ...")
    brains = api.search({},CATALOG_ANALYSIS_REQUEST_LISTING)
    total = len(brains)
    for num, brain in enumerate(brains):
        if num % 100 == 0:
            logger.info("Reseting Date Received: {}/{}".format(num, total))
        if num % TRANSACTION_THERESHOLD == 0:
            commit_transaction(portal)

        sample = api.get_object(brain)
        date_received = getTransitionDate(sample, "deliver", True)
        if date_received and date_received != sample.getDateReceived():
            sample.setDateReceived(date_received)
            sample.reindexObject(idxs=["getDateReceived", "is_received"])

    logger.info("Reseting Date Received (#233) [DONE]")
