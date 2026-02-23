"""Unit tests for cvpysdk/subclients/lotusnotes/lndbsubclient.py module."""

import pytest

from cvpysdk.subclients.lotusnotes.lndbsubclient import LNDbSubclient
from cvpysdk.subclients.lotusnotes.lnsubclient import LNSubclient


@pytest.mark.unit
class TestLNDbSubclientInheritance:
    """Tests for LNDbSubclient class hierarchy."""

    def test_inherits_lnsubclient(self):
        assert issubclass(LNDbSubclient, LNSubclient)
