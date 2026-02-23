from unittest.mock import MagicMock

import pytest

from cvpysdk.certificates import Certificate


@pytest.mark.unit
class TestCertificate:
    def test_init(self, mock_commcell):
        cert = Certificate(mock_commcell)
        assert cert.commcell is mock_commcell
        assert cert.url == mock_commcell._services["CERTIFICATES"]

    def test_make_request_success(self, mock_commcell):
        resp = MagicMock()
        resp.status_code = 200
        resp.json.return_value = {"status": "ok"}
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)

        cert = Certificate(mock_commcell)
        result = cert._make_request({"action": "test"})
        assert result == {"status": "ok"}

    def test_make_request_failure_raises(self, mock_commcell):
        resp = MagicMock()
        resp.status_code = 500
        resp.json.return_value = {"error": "server error"}
        mock_commcell._cvpysdk_object.make_request.return_value = (False, resp)

        cert = Certificate(mock_commcell)
        with pytest.raises(Exception, match="APIException"):
            cert._make_request({})
