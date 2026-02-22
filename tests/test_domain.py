#!/usr/bin/env python

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import testlib

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from cvpysdk.exception import SDKException


class DomainTest(testlib.SDKTestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def _cleanup_domain(self, domain_name):
        try:
            self.commcell_object.domains.delete(domain_name)
        except SDKException:
            pass

    def test_add_domain(self):
        self.assertRaises(SDKException, self.commcell_object.domains.get, "abc123")
        self.addCleanup(self._cleanup_domain, "automation_pyunittest")
        self.commcell_object.domains.add(
            "automation_pyunittest",
            "automation",
            "automation\\administrator",
            self.data["password1"],
            ["magic_test"],
        )
        self.assertEqual(
            "automation_pyunittest",
            self.commcell_object.domains.get("automation_pyunittest")["shortName"]["domainName"],
        )
        self.commcell_object.domains.delete("automation_pyunittest")
        self.assertRaises(
            SDKException,
            self.commcell_object.domains.get,
            "automation_pyunittest",
        )


if __name__ == "__main__":
    import unittest

    unittest.main()
