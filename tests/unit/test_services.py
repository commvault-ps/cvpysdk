import pytest

from cvpysdk.services import SERVICES_DICT_TEMPLATE, get_services

BASE_URL = "https://example.com/webconsole/api/"


@pytest.mark.unit
class TestServicesTemplate:
    def test_all_template_values_are_strings(self):
        for key, value in SERVICES_DICT_TEMPLATE.items():
            assert isinstance(value, str), f"{key} has non-string value"

    def test_all_templates_contain_placeholder(self):
        for key, value in SERVICES_DICT_TEMPLATE.items():
            assert "{0}" in value, f"{key} missing {{0}} placeholder"


@pytest.mark.unit
class TestGetServices:
    def test_get_services_returns_dict(self):
        result = get_services(BASE_URL)
        assert isinstance(result, dict)

    def test_all_urls_contain_base(self):
        result = get_services(BASE_URL)
        for key, url in result.items():
            assert url.startswith(BASE_URL), f"{key} does not start with base URL"

    def test_get_services_does_not_mutate_template(self):
        original = dict(SERVICES_DICT_TEMPLATE)
        get_services(BASE_URL)
        assert SERVICES_DICT_TEMPLATE == original

    def test_known_endpoints_exist(self):
        result = get_services(BASE_URL)
        for key in ["LOGIN", "LOGOUT", "GET_ALL_CLIENTS", "JOB", "BROWSE", "RESTORE"]:
            assert key in result, f"Missing endpoint: {key}"
