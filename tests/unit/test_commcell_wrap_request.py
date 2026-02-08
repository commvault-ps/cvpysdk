import unittest
from unittest.mock import Mock

from cvpysdk.commcell import Commcell
from cvpysdk.exception import SDKException


class TestCommcellWrapRequest(unittest.TestCase):
    def _commcell(self, services=None):
        commcell = Commcell.__new__(Commcell)
        commcell._services = services or {"GET_CLIENTS": "http://x/Client"}
        commcell._cvpysdk_object = Mock()
        return commcell

    @staticmethod
    def _response(json_value=None, content=b"resp-content", json_side_effect=None):
        response = Mock()
        response.content = content
        if json_side_effect is not None:
            response.json.side_effect = json_side_effect
        else:
            response.json.return_value = json_value
        return response

    def test_return_resp_true_and_error_check_false_returns_raw_response(self):
        commcell = self._commcell()
        response = self._response(json_value={"ok": True})
        req_kwargs = {"headers": {"X-Test": "1"}}
        commcell._cvpysdk_object.make_request.return_value = (True, response)

        result = commcell.wrap_request(
            method="GET",
            service_key="GET_CLIENTS",
            req_kwargs=req_kwargs,
            return_resp=True,
            error_check=False,
        )

        self.assertIs(result, response)
        commcell._cvpysdk_object.make_request.assert_called_once_with(
            "GET", "http://x/Client", **req_kwargs
        )

    def test_empty_check_raises_102_for_empty_json(self):
        commcell = self._commcell()
        response = self._response(json_value={})
        commcell._cvpysdk_object.make_request.return_value = (True, response)

        with self.assertRaises(SDKException) as ctx:
            commcell.wrap_request(method="GET", service_key="GET_CLIENTS", empty_check=True)

        self.assertEqual(ctx.exception.exception_module, "Response")
        self.assertEqual(ctx.exception.exception_id, "102")
        commcell._cvpysdk_object.make_request.assert_called_once_with(
            "GET", "http://x/Client"
        )

    def test_invalid_json_raises_103(self):
        commcell = self._commcell()
        response = self._response(json_side_effect=ValueError("not json"))
        commcell._cvpysdk_object.make_request.return_value = (True, response)

        with self.assertRaises(SDKException) as ctx:
            commcell.wrap_request(method="GET", service_key="GET_CLIENTS")

        self.assertEqual(ctx.exception.exception_module, "Response")
        self.assertEqual(ctx.exception.exception_id, "103")
        commcell._cvpysdk_object.make_request.assert_called_once_with(
            "GET", "http://x/Client"
        )

    def test_failed_flag_with_non_zero_error_raises_sdkexception_via_default_callback(self):
        commcell = self._commcell()
        response = self._response(
            json_value={"errorCode": 7, "errorMessage": "failed from server"}
        )
        commcell._cvpysdk_object.make_request.return_value = (False, response)

        with self.assertRaises(SDKException) as ctx:
            commcell.wrap_request(method="POST", service_key="GET_CLIENTS")

        self.assertEqual(ctx.exception.exception_module, "Response")
        self.assertEqual(ctx.exception.exception_id, "101")
        self.assertIn("[7: failed from server]", str(ctx.exception))
        commcell._cvpysdk_object.make_request.assert_called_once_with(
            "POST", "http://x/Client"
        )

    def test_custom_error_read_and_error_callback_invoked(self):
        commcell = self._commcell()
        response = self._response(json_value={"custom": "payload"})
        commcell._cvpysdk_object.make_request.return_value = (True, response)

        error_read = Mock(return_value=(42, "custom error"))
        error_callback = Mock(side_effect=SDKException("Response", "101", "custom callback"))

        with self.assertRaises(SDKException) as ctx:
            commcell.wrap_request(
                method="POST",
                service_key="GET_CLIENTS",
                error_read=error_read,
                error_callback=error_callback,
            )

        self.assertEqual(ctx.exception.exception_module, "Response")
        self.assertEqual(ctx.exception.exception_id, "101")
        error_read.assert_called_once_with({"custom": "payload"})
        error_callback.assert_called_once_with(42, "custom error")
        commcell._cvpysdk_object.make_request.assert_called_once_with(
            "POST", "http://x/Client"
        )

    def test_fill_params_formats_service_url(self):
        commcell = self._commcell(services={"GET_ONE_CLIENT": "http://x/Client/%s/%s"})
        response = self._response(json_value={"name": "client1"})
        commcell._cvpysdk_object.make_request.return_value = (True, response)
        req_kwargs = {"headers": {"Accept": "application/json"}}

        result = commcell.wrap_request(
            method="GET",
            service_key="GET_ONE_CLIENT",
            fill_params=("id", "detail"),
            req_kwargs=req_kwargs,
            empty_check=False,
        )

        self.assertEqual(result, {"name": "client1"})
        commcell._cvpysdk_object.make_request.assert_called_once_with(
            "GET", "http://x/Client/id/detail", **req_kwargs
        )


if __name__ == "__main__":
    unittest.main()
