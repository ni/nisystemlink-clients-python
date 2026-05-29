"""Tests for JsonModel alias handling."""

from inspect import signature
from typing import Annotated, cast, Literal

from nisystemlink.clients.core._uplink._json_model import JsonModel
from pydantic import AliasChoices, Field, TypeAdapter


class ExampleJsonModel(JsonModel):
    """Simple model used to verify JsonModel alias behavior."""

    program_name: str


class ExampleExplicitAliasJsonModel(JsonModel):
    """Simple model used to verify explicit alias behavior."""

    program_name: str
    session_id: str = Field(
        validation_alias=AliasChoices("session_id", "id"),
        serialization_alias="id",
    )


class TestJsonModel:
    """Test cases for JsonModel alias behavior."""

    def test__signature__uses_snake_case_field_names(self):
        """Test that constructor signatures expose Pythonic snake_case names."""
        assert str(signature(ExampleJsonModel)) == "(*, program_name: str) -> None"

    def test__snake_case_input__deserializes_and_serializes_by_alias(self):
        """Test that snake_case input remains valid and serializes to camelCase."""
        model = ExampleJsonModel(program_name="My Program")

        assert model.program_name == "My Program"
        assert model.model_dump() == {"program_name": "My Program"}
        assert model.model_dump(by_alias=True) == {"programName": "My Program"}

    def test__camel_case_input__remains_backward_compatible(self):
        """Test that legacy camelCase input remains valid."""
        model = ExampleJsonModel.model_validate({"programName": "My Program"})

        assert model.program_name == "My Program"

    def test__snake_case_input__wins_when_both_names_are_provided(self):
        """Test that Python field names remain the primary input form."""
        model = ExampleJsonModel.model_validate(
            {
                "program_name": "Preferred Program",
                "programName": "Legacy Program",
            }
        )

        assert model.program_name == "Preferred Program"

    def test__explicit_alias_signature__uses_snake_case_field_names(self):
        """Test that explicit aliases preserve snake_case constructor signatures."""
        assert str(signature(ExampleExplicitAliasJsonModel)) == (
            "(*, program_name: str, session_id: str) -> None"
        )
        assert ExampleExplicitAliasJsonModel.model_fields["session_id"].alias is None

    def test__explicit_alias__accepts_both_input_names_and_serializes_wire_name(self):
        """Test that explicit aliases accept Python and wire names and serialize wire names."""
        snake_case_model = ExampleExplicitAliasJsonModel(
            program_name="My Program",
            session_id="session-1",
        )
        camel_case_model = ExampleExplicitAliasJsonModel.model_validate(
            {"program_name": "My Program", "id": "session-2"}
        )

        assert snake_case_model.session_id == "session-1"
        assert snake_case_model.model_dump(by_alias=True) == {
            "programName": "My Program",
            "id": "session-1",
        }
        assert camel_case_model.session_id == "session-2"

    def test__identical_wire_and_python_names__do_not_create_duplicate_aliases(self):
        """Test that identical Python and wire names remain valid for discriminated unions."""

        class NotebookExecution(JsonModel):
            type: Literal["NOTEBOOK"] = Field(default="NOTEBOOK")

        class JobExecution(JsonModel):
            type: Literal["JOB"] = Field(default="JOB")

        execution_type = Annotated[
            NotebookExecution | JobExecution,
            Field(discriminator="type"),
        ]
        adapter = TypeAdapter(list[execution_type])

        parsed = cast(
            list[NotebookExecution | JobExecution],
            adapter.validate_python(
                [
                    {"type": "NOTEBOOK"},
                    {"type": "JOB"},
                ]
            ),
        )

        assert [item.type for item in parsed] == ["NOTEBOOK", "JOB"]
