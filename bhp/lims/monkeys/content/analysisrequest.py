# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Botswana Harvard Partnership (BHP)

from bhp.lims import api

def has_analyses_in_panic(self, use_objects=False):
    review_states = ("to_be_verified", "verified", "published")
    analyses = self.getAnalyses(full_objects=use_objects,
                                review_state=review_states)
    for analysis in analyses:
        if api.is_in_panic(analysis):
            return True
    return False
