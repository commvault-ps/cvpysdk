import pytest

from cvpysdk.exception import EXCEPTION_DICT, SDKException


@pytest.mark.unit
class TestSDKException:
    def test_known_module_and_id(self):
        exc = SDKException("CVPySDK", "101")
        assert str(exc) == "Failed to Login with the credentials provided"

    def test_unknown_module_raises_keyerror(self):
        with pytest.raises(KeyError):
            SDKException("NonExistent", "101")

    def test_unknown_id_raises_keyerror(self):
        with pytest.raises(KeyError):
            SDKException("CVPySDK", "999")

    def test_custom_message_appended(self):
        exc = SDKException("CVPySDK", "101", "extra")
        assert "Failed to Login with the credentials provided" in str(exc)
        assert "extra" in str(exc)
        assert "\n" in str(exc)

    def test_custom_message_replaces_empty(self):
        exc = SDKException("CVPySDK", "102", "custom")
        assert str(exc) == "custom"

    def test_exception_attributes(self):
        exc = SDKException("CVPySDK", "101")
        assert exc.exception_module == "CVPySDK"
        assert exc.exception_id == "101"
        assert exc.exception_message == "Failed to Login with the credentials provided"

    def test_all_exception_dict_entries_valid(self):
        for module, entries in EXCEPTION_DICT.items():
            assert isinstance(entries, dict), f"Module {module} value is not a dict"
            for key, value in entries.items():
                assert isinstance(key, str), f"Key {key} in {module} is not str"
                assert isinstance(value, str), f"Value for {key} in {module} is not str"

    def test_id_coerced_to_string(self):
        exc = SDKException("CVPySDK", 101)
        assert exc.exception_id == "101"
        assert str(exc) == "Failed to Login with the credentials provided"
