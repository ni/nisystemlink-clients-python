# -*- coding: utf-8 -*-

"""Implementation of TagPathUtilities."""

from typing_extensions import final


@final
class TagPathUtilities:
    """Contains helper methods for interacting with tag paths."""

    def __init_subclass__(cls) -> None:
        raise TypeError("type 'TagPathUtilities' is not an acceptable base type")

    def __init__(self) -> None:
        raise TypeError("Can't instantiate static class 'TagPathUtilities'")

    @classmethod
    def validate(cls, path: str) -> str:
        """Validate ``path`` as an input tag path.

        Clients do not typically need to call this method directly.

        Args:
            path: The tag path to validate.

        Returns:
            The validated path.

        Raises:
            ValueError: if the path is invalid.
            ValueError: if ``path`` is None.
        """
        if path is None or path.lstrip() == "":
            raise ValueError("Tag path cannot be None or empty")

        if "*" in path:
            raise ValueError("Tag path cannot contain a *")

        return path

    @classmethod
    def validate_query(cls, path: str) -> str:
        """Validate ``path`` as a tag path query.

        Clients do not typically need to call this method directly.

        Args:
            path: The tag path to validate.

        Returns:
            The validated path.

        Raises:
            ValueError: if the path is invalid.
            ValueError: if ``path`` is None.
        """
        if path is None or path.lstrip() == "":
            raise ValueError("Tag path cannot be None or empty")

        if "," in path:
            raise ValueError("Tag path cannot contain a ,")

        return path
