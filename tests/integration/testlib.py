#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright  Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Shared integration test utilities."""
import os

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from cvpysdk import commcell


class SDKTestCase(unittest.TestCase):
    """Base class for live Commcell integration tests."""

    @classmethod
    def setUpClass(cls):
        run_integration = os.environ.get('CVPYSKD_RUN_INTEGRATION') == '1' or \
            os.environ.get('CVPYSDK_RUN_INTEGRATION') == '1'

        if not run_integration:
            raise unittest.SkipTest(
                'Integration tests are disabled. Set CVPYSKD_RUN_INTEGRATION=1 to enable.'
            )

        env_mapping = {
            'webconsole_hostname': os.environ.get('CVPYSDK_WEBCONSOLE_HOSTNAME'),
            'commcell_username': os.environ.get('CVPYSDK_COMMCELL_USERNAME'),
            'commcell_password': os.environ.get('CVPYSDK_COMMCELL_PASSWORD')
        }

        missing_vars = [
            variable for variable, value in (
                ('CVPYSDK_WEBCONSOLE_HOSTNAME', env_mapping['webconsole_hostname']),
                ('CVPYSDK_COMMCELL_USERNAME', env_mapping['commcell_username']),
                ('CVPYSDK_COMMCELL_PASSWORD', env_mapping['commcell_password'])
            ) if not value
        ]

        if missing_vars:
            raise unittest.SkipTest(
                'Missing required integration environment variables: {0}'.format(
                    ', '.join(missing_vars)
                )
            )

        cls.data = {
            'commcell': env_mapping,
            'password1': os.environ.get(
                'CVPYSDK_DOMAIN_PASSWORD',
                env_mapping['commcell_password']
            )
        }

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.test_json()
        self.commcell_object = commcell.Commcell(**self.data['commcell'])

    def tearDown(self):
        self.commcell_object.logout()

    def test_json(self):
        self.assertIsInstance(self.data, dict)
        self.assertIsInstance(self.data['commcell'], dict)
        self.assertIn('webconsole_hostname', self.data['commcell'].keys())
        self.assertIn('commcell_username', self.data['commcell'].keys())
        self.assertIn('commcell_password', self.data['commcell'].keys())
        self.assertNotIn("", self.data['commcell'].values())


if __name__ == "__main__":
    unittest.main()
