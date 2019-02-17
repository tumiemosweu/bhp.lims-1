# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Botswana Harvard Partnership (BHP)

from bhp.lims.tests.base import SimpleTestCase


class TestSetup(SimpleTestCase):
    """Test Setup
    """

    def test_is_bika_lims_installed(self):
        qi = self.portal.portal_quickinstaller
        self.assertTrue(qi.isProductInstalled("bika.lims"))

    def test_is_bhp_lims_installed(self):
        qi = self.portal.portal_quickinstaller
        self.assertTrue(qi.isProductInstalled("bhp.lims"))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestSetup))
    return suite
