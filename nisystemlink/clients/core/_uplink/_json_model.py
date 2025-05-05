from pydantic import BaseModel, ConfigDict


def _camelcase(s: str) -> str:
    """Convert a snake case string to camelCase."""
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


class JsonModel(BaseModel):
    """Base class for models that are serialized to and from JSON."""

    model_config = ConfigDict(
        alias_generator=_camelcase,
        validate_by_name=True,
        validate_by_alias=True,
        extra="ignore",
    )
