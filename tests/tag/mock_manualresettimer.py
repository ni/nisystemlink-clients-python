from unittest.mock import Mock, PropertyMock

import events.events  # type: ignore
from systemlink.clients.tag._core._manual_reset_timer import ManualResetTimer


def MockManualResetTimer():  # noqa: N802
    """Construct a mock ManualResetTimer"""
    m = Mock(ManualResetTimer)
    type(m).elapsed = PropertyMock(return_value=events.events._EventSlot("elapsed"))
    type(m).__aenter__ = ManualResetTimer.__aenter__
    type(m).__aexit__ = ManualResetTimer.__aexit__
    type(m).__enter__ = ManualResetTimer.__enter__
    type(m).__exit__ = ManualResetTimer.__exit__
    return m
