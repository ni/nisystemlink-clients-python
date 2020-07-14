# -*- coding: utf-8 -*-

"""Implementation of ClasspropertySupport."""

import abc
import typing
from typing import Any, Callable, Dict, Tuple


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
    def classproperty(cls, f: Callable[[Any], Any]) -> property:
        """Make a classproperty."""
        # Cast to a property for the type checker, as we'll convert it to a property
        # later, in the __new__ method
        return typing.cast(property, cls._ClassProperty(f))
