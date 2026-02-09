#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright  Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Shared unit test utilities."""
import json
import os
import time
import sys

try:
    import unittest2 as unittest
except ImportError:
    import unittest

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(TESTS_DIR)

if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from cvpysdk import commcell
from time import sleep
from datetime import datetime, timedelta

import logging
logging.basicConfig(
    filename='unit_test.log',
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(message)s")


class SDKTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(os.path.join(TESTS_DIR, 'input.json'), 'r') as data_file:
            cls.data = json.load(data_file)

    def _has_commcell_credentials(self):
        values = self.data.get('commcell', {}).values()
        return all(value for value in values)

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.test_json()

        if not self._has_commcell_credentials():
            self.skipTest('Commcell credentials are not configured in tests/input.json')

        self.commcell_object = commcell.Commcell(**self.data['commcell'])

    def tearDown(self):
        if hasattr(self, 'commcell_object'):
            self.commcell_object.logout()

    def test_json(self):
        self.assertIsInstance(self.data, dict)
        self.assertIsInstance(self.data['commcell'], dict)
        self.assertIn('webconsole_hostname', self.data['commcell'].keys())
        self.assertIn('commcell_username', self.data['commcell'].keys())
        self.assertIn('commcell_password', self.data['commcell'].keys())


if __name__ == "__main__":
    import unittest
    unittest.main()
