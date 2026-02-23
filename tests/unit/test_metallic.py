import pytest

from cvpysdk.exception import SDKException
from cvpysdk.metallic import Metallic


@pytest.mark.unit
class TestMetallic:
    """Tests for the Metallic class."""

    def test_init(self, mock_commcell):
        metallic = Metallic(mock_commcell)
        assert metallic._commcell_object is mock_commcell
        assert metallic._metallic_details is None
        assert metallic._metallic_web_url is None
        assert metallic._metallic_obj is None
        assert metallic._cloudservices_details is None

    def test_metallic_commcell_object_bad_types_raises(self, mock_commcell):
        metallic = Metallic(mock_commcell)
        with pytest.raises(SDKException):
            metallic._metallic_commcell_object(123, "user", "pass")

    def test_metallic_commcell_object_bad_username_raises(self, mock_commcell):
        metallic = Metallic(mock_commcell)
        with pytest.raises(SDKException):
            metallic._metallic_commcell_object("host", 123, "pass")

    def test_metallic_commcell_object_bad_password_raises(self, mock_commcell):
        metallic = Metallic(mock_commcell)
        with pytest.raises(SDKException):
            metallic._metallic_commcell_object("host", "user", 123)

    def test_metallic_subscribe_bad_types_raises(self, mock_commcell):
        metallic = Metallic(mock_commcell)
        with pytest.raises(SDKException):
            metallic.metallic_subscribe(123, "user", "pass")

    def test_metallic_subscribe_bad_company_type_raises(self, mock_commcell):
        metallic = Metallic(mock_commcell)
        with pytest.raises(SDKException):
            metallic.metallic_subscribe("host", "user", "pass", msp_company_name=123)
