# -*- coding: utf-8 -*-

"""Implementation of ApiError."""

import typing
from typing import Any, Dict, Iterable, List, Optional

from typing_extensions import final


@final
class ApiError:
    """Represents the standard error structure for SystemLink API responses."""

    def __init_subclass__(cls) -> None:
        raise TypeError("type 'ApiError' is not an acceptable base type")

    def __init__(self) -> None:
        self._name = None  # type: Optional[str]
        self._code = None  # type: Optional[int]
        self._message = None  # type: Optional[str]
        self._args = []  # type: List[str]
        self._resource_type = None  # type: Optional[str]
        self._resource_id = None  # type: Optional[str]
        self._inner_errors = []  # type: List[ApiError]

    @property
    def name(self) -> Optional[str]:  # noqa: D401
        """The name of the error."""
        return self._name

    @name.setter
    def name(self, value: Optional[str]) -> None:
        self._name = value

    @property
    def code(self) -> Optional[int]:  # noqa: D401
        """The numeric code associated with the error."""
        return self._code

    @code.setter
    def code(self, value: Optional[int]) -> None:
        self._code = value

    @property
    def message(self) -> Optional[str]:  # noqa: D401
        """The error message."""
        return self._message

    @message.setter
    def message(self, value: Optional[str]) -> None:
        self._message = value

    @property
    def args(self) -> List[str]:  # noqa: D401
        """The list of positional arguments formatted into the error."""
        return self._args

    @args.setter
    def args(self, value: Iterable[str]) -> None:
        self._args = list(value)

    @property
    def resource_type(self) -> Optional[str]:  # noqa: D401
        """The type of resource associated with the error, if any.

        Set this when setting :attr:`resource_id`.
        """
        return self._resource_type

    @resource_type.setter
    def resource_type(self, value: Optional[str]) -> None:
        self._resource_type = value

    @property
    def resource_id(self) -> Optional[str]:  # noqa: D401
        """The ID of the resource associated with the error, if any.

        Set :attr:`resource_type` when setting this property.
        """
        return self._resource_id

    @resource_id.setter
    def resource_id(self, value: Optional[str]) -> None:
        self._resource_id = value

    @property
    def inner_errors(self) -> List["ApiError"]:  # noqa: D401
        """The list of inner errors."""
        return self._inner_errors

    @inner_errors.setter
    def inner_errors(self, value: Iterable["ApiError"]) -> None:
        self._inner_errors = list(value)

    def copy(self) -> "ApiError":
        """Get a copy of this object."""
        new = ApiError()
        new.name = self.name
        new.code = self.code
        new.message = self.message
        new.args = self.args
        new.resource_type = self.resource_type
        new.resource_id = self.resource_id
        new.inner_errors = self.inner_errors
        return new

    def __str__(self) -> str:
        txt = ""
        if self._name:
            txt += "Name: {}\n".format(self._name)
        if self._code:
            txt += "Code: {}\n".format(self._code)
        if self._message:
            txt += "Message: {}\n".format(self._message)
        if self._args:
            args = "\n  ".join(self._args)
            txt += "Args:\n  {}\n".format(args)
        if self._resource_type:
            txt += "Resource Type: {}\n".format(self._resource_type)
        if self._resource_id:
            txt += "Resource Id: {}\n".format(self._resource_id)
        if self._inner_errors:
            inner_errors = "\n  ".join(str(e) for e in self._inner_errors)
            txt += "Inner Errors:\n  {}\n".format(
                str(inner_errors).replace("\n", "\n  ")
            )
        return txt[:-1]

    def __repr__(self) -> str:
        return (
            "ApiError(name={!r}, code={!r}, message={!r}, args={!r}, "
            "resource_type={!r}, resource_id={!r}, inner_errors={!r})".format(
                self.name,
                self.code,
                self.message,
                self.args,
                self.resource_type,
                self.resource_id,
                self.inner_errors,
            )
        )

    def __eq__(self, other: object) -> bool:
        other_ = typing.cast(ApiError, other)
        return all(
            (
                isinstance(other, ApiError),
                self.name == other_.name,
                self.code == other_.code,
                self.message == other_.message,
                self.args == other_.args,
                self.resource_type == other_.resource_type,
                self.resource_id == other_.resource_id,
                self.inner_errors == other_.inner_errors,
            )
        )

    def __hash__(self) -> int:
        return hash(
            (
                self.name,
                self.code,
                self.message,
                tuple(self.args),
                self.resource_type,
                self.resource_id,
                tuple(self.inner_errors),
            )
        )

    @classmethod
    def from_json_dict(cls, data: Dict[str, Any]) -> "ApiError":
        err = cls()
        err.name = data.get("name")
        err.code = data.get("code")
        err.message = data.get("message")
        err.args = data.get("args", [])
        err.resource_type = data.get("resourceType")
        err.resource_id = data.get("resourceId")
        err.inner_errors = [cls.from_json_dict(e) for e in data.get("innerErrors", [])]
        return err
