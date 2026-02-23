#!/usr/bin/env python

# --------------------------------------------------------------------------
# Copyright  Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Shared unit test utilities."""

import json
import logging
import unittest

from cvpysdk import commcell

logging.basicConfig(
    filename="unit_test.log", level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s"
)


class SDKTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open("input.json") as data_file:
            cls.data = json.load(data_file)

    def setUp(self):
        unittest.TestCase.setUp(self)
        self._validate_json_config()
        self.commcell_object = commcell.Commcell(**self.data["commcell"])

    def tearDown(self):
        self.commcell_object.logout()

    def _validate_json_config(self):
        self.assertIsInstance(self.data, dict)
        self.assertIsInstance(self.data["commcell"], dict)
        self.assertIn("webconsole_hostname", self.data["commcell"].keys())
        self.assertIn("commcell_username", self.data["commcell"].keys())
        self.assertIn("commcell_password", self.data["commcell"].keys())
        self.assertNotIn("", self.data["commcell"].values())


if __name__ == "__main__":
    import unittest

    unittest.main()
