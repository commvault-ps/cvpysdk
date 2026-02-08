#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Runs CVPySDK tests. Unit tests run by default; integration tests are opt-in."""

import os
import sys

try:
    import unittest2 as unittest
except ImportError:
    import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

def _discover_suite(start_dir):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return unittest.defaultTestLoader.discover(
        start_dir=os.path.join(root_dir, start_dir),
        pattern='test*.py',
        top_level_dir=root_dir
    )


def _run_integration_enabled():
    return os.environ.get('CVPYSKD_RUN_INTEGRATION') == '1' or \
        os.environ.get('CVPYSDK_RUN_INTEGRATION') == '1'


def build_suite():
    suite = unittest.TestSuite()
    suite.addTests(_discover_suite('unit'))

    if _run_integration_enabled():
        suite.addTests(_discover_suite('integration'))

    return suite


if __name__ == '__main__':
    unittest.TextTestRunner().run(build_suite())
