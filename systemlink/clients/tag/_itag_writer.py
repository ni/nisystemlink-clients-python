# -*- coding: utf-8 -*-

"""Implementation of ITagWriter."""

import abc
import datetime
import typing
from typing import Any, Awaitable, Dict, Optional, Tuple, Union

from systemlink.clients import tag as tbase
from systemlink.clients.core._internal._timestamp_utilities import TimestampUtilities
from typing_extensions import Literal


_VALID_TYPES = {
    tbase.DataType.BOOLEAN: bool,
    tbase.DataType.DATE_TIME: datetime.datetime,
    tbase.DataType.DOUBLE: (float, int),
    tbase.DataType.INT32: int,
    tbase.DataType.UINT64: int,
    tbase.DataType.STRING: str,
}  # type: Dict[tbase.DataType, Union[type, Tuple[type, type]]]


class _ITagWriterOverloads(abc.ABC):
    """Contains the overloaded methods of ITagWriter.

    These overloads exist so that ``mypy`` can validate proper data types are used when
    writing tag values, as long as a literal DataType enum value is given when calling
    :meth:`get_tag_writer`. But they are hidden away in a base class so that they aren't
    documented by Sphinx, because Sphinx doesn't properly recognize the type annotations
    of overloads. See also: https://github.com/sphinx-doc/sphinx/issues/7901
    """

    @typing.overload
    def get_tag_writer(
        self, path: str, data_type: Literal[tbase.DataType.BOOLEAN]
    ) -> "tbase.TagValueWriter[bool]":
        pass

    @typing.overload
    def get_tag_writer(
        self, path: str, data_type: Literal[tbase.DataType.DATE_TIME]
    ) -> "tbase.TagValueWriter[datetime.datetime]":
        pass

    @typing.overload
    def get_tag_writer(
        self, path: str, data_type: Literal[tbase.DataType.DOUBLE]
    ) -> "tbase.TagValueWriter[float]":
        pass

    @typing.overload
    def get_tag_writer(
        self, path: str, data_type: Literal[tbase.DataType.INT32]
    ) -> "tbase.TagValueWriter[int]":
        pass

    @typing.overload
    def get_tag_writer(
        self, path: str, data_type: Literal[tbase.DataType.UINT64]
    ) -> "tbase.TagValueWriter[int]":
        pass

    @typing.overload
    def get_tag_writer(
        self, path: str, data_type: Literal[tbase.DataType.STRING]
    ) -> "tbase.TagValueWriter[str]":
        pass

    @typing.overload
    def get_tag_writer(
        self, path: str, data_type: tbase.DataType
    ) -> "tbase.TagValueWriter[Any]":
        pass

    def get_tag_writer(
        self, path: str, data_type: tbase.DataType
    ) -> "tbase.TagValueWriter":
        """Get a :class:`TagValueWriter` for this path.

        Args:
            path: The path of the tag to write.
            data_type: The data type of the tag to write.
        """
        return self._get_tag_writer(path, data_type)

    @abc.abstractmethod
    def _get_tag_writer(
        self, path: str, data_type: tbase.DataType
    ) -> "tbase.TagValueWriter":
        """Get a :class:`TagValueWriter` for this path.

        Args:
            path: The path of the tag to write.
            data_type: The data type of the tag to write.
        """
        ...


class ITagWriter(_ITagWriterOverloads):
    """Provides an interface for writing the current value of a single SystemLink tag."""

    def write(
        self,
        path: str,
        data_type: tbase.DataType,
        value: Union[bool, int, float, str, datetime.datetime],
        *,
        timestamp: Optional[datetime.datetime] = None
    ) -> None:
        """Write a tag's value.

        Args:
            path: The path of the tag to write.
            data_type: The data type of the value to write.
            value: The tag value to write.
            timestamp: A custom timestamp to associate with the value, or None to have
                the server specify the timestamp.

        Raises:
            ValueError: if ``path`` is empty or invalid.
            ValueError: if ``path`` or ``value`` is None.
            ValueError: if ``data_type`` is invalid.
            ValueError: if ``value`` has the wrong data type.
            ReferenceError: if the writer has been closed.
            ApiException: if the API call fails.
        """
        self._validate_type(value, data_type)

        if data_type == tbase.DataType.DATE_TIME:
            value = TimestampUtilities.datetime_to_str(
                typing.cast(datetime.datetime, value)
            )

        self._write(path, data_type, str(value), timestamp)

    def write_async(
        self,
        path: str,
        data_type: tbase.DataType,
        value: str,
        *,
        timestamp: Optional[datetime.datetime] = None
    ) -> Awaitable[None]:
        """Asynchronously write a tag's value.

        Args:
            path: The path of the tag to write.
            data_type: The data type of the value to write.
            value: The tag value to write.
            timestamp: A custom timestamp to associate with the value, or None to have
                the server specify the timestamp.

        Returns:
            A task representing the asynchronous operation.

        Raises:
            ValueError: if ``path`` is empty or invalid.
            ValueError: if ``path`` or ``value`` is None.
            ValueError: if ``data_type`` is invalid.
            ValueError: if ``value`` has the wrong data type.
            ReferenceError: if the writer has been closed.
            ApiException: if the API call fails.
        """
        self._validate_type(value, data_type)

        if data_type == tbase.DataType.DATE_TIME:
            value = TimestampUtilities.datetime_to_str(
                typing.cast(datetime.datetime, value)
            )

        return self._write_async(path, data_type, str(value), timestamp)

    @classmethod
    def _validate_type(
        cls,
        value: Union[bool, int, float, str, datetime.datetime],
        data_type: tbase.DataType,
    ) -> None:
        if data_type == tbase.DataType.UNKNOWN:
            raise ValueError("data_type is UNKNOWN")

        if not isinstance(value, _VALID_TYPES[data_type]):
            raise ValueError(
                "value has wrong python data type ({}) for SystemLink data type {}".format(
                    type(value).__name__, data_type.name
                )
            )

        # python's bool is a subclass of int, so the above check won't catch some cases
        if isinstance(value, bool) and data_type != tbase.DataType.BOOLEAN:
            raise ValueError(
                "value has wrong python data type ({}) for SystemLink data type {}".format(
                    type(value).__name__, data_type.name
                )
            )

        if data_type == tbase.DataType.INT32:
            assert isinstance(value, int)
            if not -(2 ** 31) <= value < 2 ** 31:
                raise ValueError(
                    "value {} is not the valid range of an INT32".format(value)
                )
        elif data_type == tbase.DataType.UINT64:
            assert isinstance(value, int)
            if not 0 <= value < 2 ** 64:
                raise ValueError(
                    "value {} is not the valid range of a UINT64".format(value)
                )

    @abc.abstractmethod
    def _write(
        self,
        path: str,
        data_type: tbase.DataType,
        value: str,
        timestamp: Optional[datetime.datetime] = None,
    ) -> None:
        """Write a tag's value that's been serialized to a string.

        Args:
            path: The path of the tag to write.
            data_type: The data type of the value to write.
            value: The tag value to write, serialized as a string.
            timestamp: A custom timestamp to associate with the value, or None to have
                the server specify the timestamp.

        Raises:
            ValueError: if ``path`` is empty or invalid.
            ValueError: if ``path`` or ``value`` is None.
            ValueError: if ``data_type`` is invalid.
            ReferenceError: if the writer has been closed.
            ApiException: if the API call fails.
        """
        ...

    @abc.abstractmethod
    async def _write_async(
        self,
        path: str,
        data_type: tbase.DataType,
        value: str,
        timestamp: Optional[datetime.datetime] = None,
    ) -> None:
        """Asynchronously write a tag's value that's been serialized to a string.

        Args:
            path: The path of the tag to write.
            data_type: The data type of the value to write.
            value: The tag value to write, serialized as a string.
            timestamp: A custom timestamp to associate with the value, or None to have
                the server specify the timestamp.

        Returns:
            A task representing the asynchronous operation.

        Raises:
            ValueError: if ``path`` is empty or invalid.
            ValueError: if ``path`` or ``value`` is None.
            ValueError: if ``data_type`` is invalid.
            ReferenceError: if the writer has been closed.
            ApiException: if the API call fails.
        """
        ...

    def _get_tag_writer(
        self, path: str, data_type: tbase.DataType
    ) -> "tbase.TagValueWriter":
        """Get a :class:`TagValueWriter` for this path.

        Args:
            path: The path of the tag to write.
            data_type: The data type of the tag to write.
        """
        return tbase.TagValueWriter(self, tbase.TagData(path, data_type))
