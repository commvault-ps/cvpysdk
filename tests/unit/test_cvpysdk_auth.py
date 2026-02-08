#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from unittest.mock import Mock, patch

from cvpysdk.cvpysdk import CVPySDK
from cvpysdk.exception import SDKException


class FakeCommcell:
    """Minimal commcell test double used by CVPySDK auth tests."""

    def __init__(self):
        self._services = {
            'LOGIN': 'https://example/login',
            'RENEW_LOGIN_TOKEN': 'https://example/renew',
        }
        self._headers = {'Authtoken': 'old-token'}
        self._user = 'test_user'
        self._password = 'test_password'
        self.device_id = 'device-1'
        self.is_service_commcell = False
        self._is_saml_login = False
        self.master_commcell = None
        self.master_saml_token = 'master-token'

    @staticmethod
    def _update_response_(response_text):
        return 'updated: {0}'.format(response_text)


class CVPySDKAuthTest(unittest.TestCase):

    def setUp(self):
        self.commcell = FakeCommcell()
        self.sdk = CVPySDK(self.commcell)

    @staticmethod
    def _response(json_payload, text='response-text'):
        response = Mock()
        response.json.return_value = json_payload
        response.text = text
        return response

    def test_login_success_returns_token(self):
        response = self._response({'userName': 'user1', 'token': 'token-abc'})

        with patch.object(self.sdk, 'make_request', return_value=(True, response)):
            token = self.sdk._login()

        self.assertEqual(token, 'token-abc')

    def test_login_account_locked_raises_sdkexception_with_lock_duration(self):
        response = self._response({
            'errList': [{'errLogMessage': 'account locked'}],
            'isAccountLocked': True,
            'remainingLockTime': 7260,
        })

        with patch.object(self.sdk, 'make_request', return_value=(True, response)):
            with self.assertRaises(SDKException) as context:
                self.sdk._login()

        exception = context.exception
        self.assertEqual(exception.exception_module, 'CVPySDK')
        self.assertEqual(exception.exception_id, '101')
        self.assertIn('User account is locked for 2 hour(s) 1 minute(s).', str(exception))

    def test_login_ssl_access_denied_raises_ssl_guidance_error(self):
        response = self._response(
            {'errorMessage': 'Access denied by policy', 'errorCode': 5},
            text='access denied'
        )

        with patch.object(self.sdk, 'make_request', return_value=(False, response)):
            with self.assertRaises(SDKException) as context:
                self.sdk._login()

        exception = context.exception
        self.assertEqual(exception.exception_module, 'Response')
        self.assertEqual(exception.exception_id, '101')
        self.assertIn('problem with the SSL certificate', str(exception))

    def test_login_empty_json_raises_response_102(self):
        response = self._response({})

        with patch.object(self.sdk, 'make_request', return_value=(True, response)):
            with self.assertRaises(SDKException) as context:
                self.sdk._login()

        exception = context.exception
        self.assertEqual(exception.exception_module, 'Response')
        self.assertEqual(exception.exception_id, '102')

    def test_renew_login_token_returns_new_token(self):
        response = self._response({'token': 'new-token'})

        with patch.object(self.sdk, 'make_request', return_value=(True, response)):
            token = self.sdk._renew_login_token(attempts=1)

        self.assertEqual(token, 'new-token')

    def test_renew_login_token_saml_missing_master_commcell_raises_106(self):
        self.commcell._is_saml_login = True
        self.commcell.master_commcell = None

        with self.assertRaises(SDKException) as context:
            self.sdk._renew_login_token(attempts=0)

        exception = context.exception
        self.assertEqual(exception.exception_module, 'CVPySDK')
        self.assertEqual(exception.exception_id, '106')

    def test_renew_login_token_unsuccessful_raises_108(self):
        response = self._response({'error': 'failed'}, text='renew-failed')

        with patch.object(self.sdk, 'make_request', return_value=(False, response)):
            with self.assertRaises(SDKException) as context:
                self.sdk._renew_login_token(attempts=3)

        exception = context.exception
        self.assertEqual(exception.exception_module, 'CVPySDK')
        self.assertEqual(exception.exception_id, '108')
        self.assertIn('updated: renew-failed', str(exception))


if __name__ == '__main__':
    unittest.main()
