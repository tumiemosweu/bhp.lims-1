# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Botswana Harvard Partnership (BHP)

from Products.Archetypes.utils import DisplayList

PRODUCT_NAME = "bhp.lims"

GENDERS = DisplayList((
    ('m', "Male"),
    ('f', "Female"),
))

GENDERS_ANY = DisplayList((
    ('a', "Any"),
    ('m', "Male"),
    ('f', "Female"),
))

PRIORITIES = DisplayList((
    ('1', 'Urgent'),
    ('3', 'Routine'),
    ('5', 'STAT'),
))

CODES = DisplayList((
    ('',''),
    ('screening','Screening'),
    ('entry','Entry'),
    ('infusion','Infusion'),
    ('pre_infusion','Pre-Infusion'),
    ('post_infusion','Post-Infusion'),
    ('day','Day'),
    ('week','Week'),
    ('month','Month'),
    ('delivery','Delivery')
))

GRADES_KEYS = (
    "G1_low_min",
    "G1_low_max",
    "G1_high_min",
    "G1_high_max",
    "G2_low_min",
    "G2_low_max",
    "G2_high_min",
    "G2_high_max",
    "G3_low_min",
    "G3_low_max",
    "G3_high_min",
    "G3_high_max",
    "G4_low_min",
    "G4_low_max",
    "G4_high_min",
    "G4_high_max",
)