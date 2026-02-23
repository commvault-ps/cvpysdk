"""Unit tests for cvpysdk/subclients/lotusnotes/lndmsubclient.py module."""

import pytest

from cvpysdk.subclients.lotusnotes.lndmsubclient import LNDmSubclient
from cvpysdk.subclients.lotusnotes.lnsubclient import LNSubclient


@pytest.mark.unit
class TestLNDmSubclientInheritance:
    """Tests for LNDmSubclient class hierarchy."""

    def test_inherits_lnsubclient(self):
        assert issubclass(LNDmSubclient, LNSubclient)
