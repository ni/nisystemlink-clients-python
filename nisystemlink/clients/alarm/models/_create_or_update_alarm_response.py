from nisystemlink.clients.core._uplink._json_model import JsonModel


class CreateOrUpdateAlarmResponse(JsonModel):
    """Contains the result of creating or updating an alarm."""

    instance_id: str
    """The ID of the created or modified alarm."""
