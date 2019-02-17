# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Botswana Harvard Partnership (BHP)

def get_progress_percentage(self, ar_brain):
    """Returns the percentage of completeness of the Analysis Request
    """
    weights = {
        "sample_ordered": 0,
        "sample_shipped": 10,
        "sample_at_reception": 20,
        "sample_due": 30,
        "sample_received": 40,
        "to_be_verified": 70,
        "verified": 90,
        "published": 100
    }

    min_val = weights["sample_received"]
    max_val = weights["verified"]
    progress = weights.get(ar_brain.review_state, 0)
    if progress < min_val or progress >= max_val:
        return progress

    diff_val = max_val - min_val
    numbers = ar_brain.getAnalysesNum
    num_analyses = numbers[1] or 0
    if not num_analyses:
        return min_val

    # [verified, total, not_submitted, to_be_verified]
    num_to_be_verified = numbers[3] or 0
    num_verified = numbers[0] or 0

    # 2 steps per analysis (submit, verify)
    max_num_steps = (num_analyses * 2) + 1
    num_steps = num_to_be_verified + (num_verified * 2)
    if not num_steps:
        return min_val
    if num_steps > max_num_steps:
        return max_val
    return ((num_steps * diff_val) / max_num_steps) + min_val
