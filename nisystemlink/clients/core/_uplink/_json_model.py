from pydantic import AliasChoices, AliasGenerator, BaseModel, ConfigDict


def _camelcase(s: str) -> str:
    """Convert a snake case string to camelCase."""
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


def _validation_aliases(s: str) -> str | AliasChoices:
    """Accept both Python snake_case and wire-format camelCase inputs."""
    camelcase = _camelcase(s)
    if camelcase == s:
        return s
    return AliasChoices(s, camelcase)


class JsonModel(BaseModel):
    """Base class for models that are serialized to and from JSON."""

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=_validation_aliases,
            serialization_alias=_camelcase,
        ),
        validate_by_name=True,
        validate_by_alias=True,
        extra="ignore",
    )
