# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Botswana Harvard Partnership (BHP)

from bhp.lims import api

def has_analyses_in_panic(self):
    analyses = self.getAnalyses(full_objects=True, retracted=False)
    for analysis in analyses:
        if api.is_in_panic(analysis):
            return True
    return False
