# -*- coding: utf-8 -*-

"""Implementation of ClasspropertySupport."""

import abc
import typing
from typing import Any, Callable, Dict, Tuple, TypeVar

_T = TypeVar("_T")


class ClasspropertySupport(abc.ABCMeta):
    """Meta class for classes that cannot be subclassed."""

    class _ClassProperty:
        def __init__(self, func: Callable[[Any], Any]):
            self.func = func

    def __new__(
        meta, name: str, bases: Tuple[type, ...], dct: Dict[str, Any]
    ) -> "ClasspropertySupport":
        class ClasspropertySupport_(meta):  # type: ignore
            pass

        for k, v in dct.items():
            # Promote all instance properties to be class properties
            if isinstance(v, meta._ClassProperty):
                setattr(ClasspropertySupport_, k, property(v.func))

        return typing.cast(
            ClasspropertySupport,
            super().__new__(ClasspropertySupport_, name, bases, dct),
        )

    @classmethod
    def classproperty(cls, f: Callable[[Any], _T]) -> _T:
        """Make a classproperty."""
        # Cast to preserve the original function's return type for the type checker.
        # It'll get wrapped in a property in the __new__ method.
        return typing.cast(_T, cls._ClassProperty(f))
