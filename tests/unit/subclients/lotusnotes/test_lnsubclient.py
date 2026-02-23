"""Unit tests for cvpysdk/subclients/lotusnotes/lnsubclient.py module."""

import pytest

from cvpysdk.subclient import Subclient
from cvpysdk.subclients.lotusnotes.lnsubclient import LNSubclient


@pytest.mark.unit
class TestLNSubclientInheritance:
    """Tests for LNSubclient class hierarchy."""

    def test_inherits_subclient(self):
        assert issubclass(LNSubclient, Subclient)
