from pydantic import BaseModel, Extra


def _camelcase(s: str) -> str:
    """Convert a snake case string to camelCase."""
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


class JsonModel(BaseModel):
    """Base class for models that are serialized to and from JSON."""

    class Config:
        alias_generator = _camelcase
        allow_population_by_field_name = True
        extra = Extra.ignore
