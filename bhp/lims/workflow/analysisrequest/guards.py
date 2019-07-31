# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Botswana Harvard Partnership (BHP)

from AccessControl.SecurityInfo import ModuleSecurityInfo
from bhp.lims import api

security = ModuleSecurityInfo(__name__)

@security.public
def guard_send_to_lab(analysis_request):
    """ Guard for send_to_lab transition. Returns true if the current user is
    a client contact, the Sample (context) is active and it belongs to the same
    client.
    """
    if api.is_client_contact():
        user = api.get_current_user()
        client = analysis_request.getClient()
        if not client.getContactFromUsername(user.id):
            return False
    return True


@security.public
def guard_deliver(analysis_request):
    """Guard for deliver transition. Returns true if a Courier has been 
    assigned to the Sample and the Sample (context) is active. Note we
    do not check for roles or client here because permissions for clients
    when the sample is in state `sample_shipped` are already defined in the
    workflow definition.
    """
    # If sample does not have a courier assigned, we cannot deliver
    # TODO Need to deal with Courier Schema field from Sample
    if not analysis_request.Schema()['Courier'].get(analysis_request):
        return False
    # If the current user is a Client contact, do not allow to
    return not api.is_client_contact()


@security.public
def guard_process(analysis_request):
    """Guard for process (partitioning) process
    Only Primary Analysis Requests can be partitioned
    """
    # If the sample is not a primary sample, do not allow processing
    if analysis_request.isPartition():
        return False
    # If the current user is a Client contact, do not allow processing
    return not api.is_client_contact()


@security.public
def guard_send_to_pot(analysis_request):
    """Guard for sending the sample to the point of testing
    """
    # Do not allow if the current user is a Client contact
    return not api.is_client_contact()


@security.public
def guard_receive_at_pot(analysis_request):
    """Guard for reception of the sample at the point of testing
    """
    # TODO Need to ask. Not all analyses might be set in partitions!
    # The sample cannot be received at point of testing unless all partitions
    # it contains has been received already
    #bhp_states = ["sample_ordered",
    #              "sample_shipped",
    #              "sample_at_reception",
    #              "sample_due"]
    #not_received = filter(lambda d: api.get_workflow_status_of(d) in bhp_states,
    #                      analysis_request.getDescendants())
    #if not_received:
    #    return False

    # Do not allow if the current user is a Client contact
    return not api.is_client_contact()


@security.public
def guard_dettach(analysis_request):
    """Guard dettach partition
    """
    # Dettach transition can only be done to partitions
    if not analysis_request.isPartition():
        return False
    # If the current user is a Client contact, do not allow to dettach
    return not api.is_client_contact()

