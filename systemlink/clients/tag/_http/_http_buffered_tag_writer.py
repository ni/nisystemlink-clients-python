# -*- coding: utf-8 -*-

"""Implementation of HttpBufferedTagWriter."""

import datetime
from collections import OrderedDict
from typing import Any, Dict, Optional

from systemlink.clients import tag as tbase
from systemlink.clients.core._internal._http_client import HttpClient
from systemlink.clients.core._internal._timestamp_utilities import TimestampUtilities
from systemlink.clients.tag._core._itime_stamper import ITimeStamper
from systemlink.clients.tag._core._manual_reset_timer import ManualResetTimer
from typing_extensions import final


@final
class HttpBufferedTagWriter(tbase.BufferedTagWriter):
    def __init_subclass__(cls) -> None:
        raise TypeError("type 'HttpBufferedTagWriter' is not an acceptable base type")

    def __init__(
        self,
        client: HttpClient,
        stamper: ITimeStamper,
        buffer_size: int,
        flush_timer: ManualResetTimer,
    ) -> None:
        super().__init__(stamper, buffer_size, flush_timer)
        self._api = client.at_uri("/nitag/v2")
        self._buffer = OrderedDict()  # type: OrderedDict[str, Dict[str, Any]]

    def _buffer_value(self, path: str, value: Dict[str, Any]) -> None:
        if path not in self._buffer:
            self._buffer.setdefault(path, {"path": path, "updates": []})
        self._buffer[path]["updates"].append(value)

    def _clear_buffer(self) -> None:
        self._buffer.clear()

    def _copy_buffer(self) -> Dict[str, Dict[str, Any]]:
        updates = self._buffer
        self._buffer = OrderedDict()
        return updates

    def _create_item(
        self,
        path: str,
        data_type: tbase.DataType,
        value: str,
        timestamp: Optional[datetime.datetime] = None,
    ) -> Dict[str, Any]:
        item = {
            "value": {"value": value, "type": data_type.api_name}
        }  # type: Dict[str, Any]
        if timestamp is not None:
            item["timestamp"] = TimestampUtilities.datetime_to_str(timestamp)
        return item

    def _send_writes(self, updates: Dict[str, Dict[str, Any]]) -> None:
        self._api.post("/update-current-values", data=list(updates.values()))

    async def _send_writes_async(self, updates: Dict[str, Any]) -> None:
        await self._api.as_async.post(
            "/update-current-values", data=list(updates.values())
        )
