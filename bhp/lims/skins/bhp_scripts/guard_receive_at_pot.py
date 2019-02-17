# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Botswana Harvard Partnership (BHP)

## Script (Python) "guard_receive_to_pot"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

from bhp.lims.workflow.analysisrequest.guards import guard_receive_at_pot
return guard_receive_at_pot(context)
