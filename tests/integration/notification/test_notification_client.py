import pytest
from nisystemlink.clients.core import ApiException
from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.notification import NotificationClient
from nisystemlink.clients.notification.models import (
    AddressFields,
    AddressGroup,
    DynamicStrategyRequest,
    MessageFieldTemplates,
    MessageTemplate,
    NotificationConfiguration,
    NotificationStrategy,
)


@pytest.fixture
def request_model():
    """Returns the created request."""
    _address_group = AddressGroup(
        id="address_group_id",
        interpreting_service_name="smtp",
        display_name="name",
        properties={"property": "value"},
        fields={
            AddressFields.toAddresses: ["address1@example.com"],
            AddressFields.ccAddresses: ["address2@example.com"],
            AddressFields.bccAddresses: ["address3@example.com"],
        },
        referencing_notification_strategies=["reference_notification_strategy"],
    )

    _message_template = MessageTemplate(
        id="address_group_id",
        interpreting_service_name="smtp",
        display_name="name",
        properties={"property": "value"},
        fields={
            MessageFieldTemplates.subjectTemplate: "subject",
            MessageFieldTemplates.bodyTemplate: "body",
        },
        referencing_notification_strategies=["reference_notification_strategy"],
    )

    _notification_configuration = NotificationConfiguration(
        address_group_id="address_group_id",
        message_template_id="message_template_id",
        address_group=_address_group,
        message_template=_message_template,
    )

    _notification_strategy = NotificationStrategy(
        notification_configurations=[
            _notification_configuration,
        ]
    )

    _dynamic_strategy_request = DynamicStrategyRequest(
        message_template_substitution_fields={"replacement": "value"},
        notification_strategy=_notification_strategy,
    )

    return _dynamic_strategy_request


@pytest.fixture(scope="class")
def client(enterprise_config: HttpConfiguration) -> NotificationClient:
    """Fixture to create a Notification client."""
    return NotificationClient(enterprise_config)


@pytest.mark.integration
@pytest.mark.enterprise
class TestNotificationClient:
    def test__apply_strategy_with_correct_request__returns_none(
        self, client: NotificationClient, request_model: DynamicStrategyRequest
    ):
        assert client.apply_notification_strategy(request=request_model) is None

    def test__apply_strategy_with_empty_template_substitution_fields__raises_exception(
        self, client: NotificationClient, request_model: DynamicStrategyRequest
    ):
        request_model.message_template_substitution_fields = None  # type: ignore[assignment]

        with pytest.raises(ApiException):
            client.apply_notification_strategy(request=request_model)

    def test__apply_strategy_with_no_recipient__raises_exception(
        self, client: NotificationClient, request_model: DynamicStrategyRequest
    ):
        request_model.notification_strategy.notification_configurations[
            0
        ].address_group.fields = {}

        with pytest.raises(ApiException):
            client.apply_notification_strategy(request=request_model)

    def test__apply_strategy_with_invalid_recipient__raises_exception(
        self, client: NotificationClient, request_model: DynamicStrategyRequest
    ):
        request_model.notification_strategy.notification_configurations[
            0
        ].address_group.fields = {AddressFields.toAddresses: ["sample"]}

        with pytest.raises(ApiException):
            client.apply_notification_strategy(request=request_model)

    def test__apply_strategy_with_no_configurations__raises_exception(
        self, client: NotificationClient, request_model: DynamicStrategyRequest
    ):
        request_model.notification_strategy.notification_configurations = []

        with pytest.raises(ApiException):
            client.apply_notification_strategy(request=request_model)

    def test__apply_strategy_with_empty_address_groups__raises_exception(
        self, client: NotificationClient, request_model: DynamicStrategyRequest
    ):
        request_model.notification_strategy.notification_configurations[
            0
        ].address_group = None  # type: ignore[assignment]

        with pytest.raises(ApiException):
            client.apply_notification_strategy(request=request_model)

    def test__apply_strategy_with_empty_message_template__raises_exception(
        self, client: NotificationClient, request_model: DynamicStrategyRequest
    ):
        request_model.notification_strategy.notification_configurations[
            0
        ].message_template = None  # type: ignore[assignment]

        with pytest.raises(ApiException):
            client.apply_notification_strategy(request=request_model)

    def test__apply_strategy_with_invalid_message_template_fields__raises_exception(
        self, client: NotificationClient, request_model: DynamicStrategyRequest
    ):
        request_model.notification_strategy.notification_configurations[
            0
        ].message_template.fields = {MessageFieldTemplates.bodyTemplate: "body"}

        with pytest.raises(ApiException):
            client.apply_notification_strategy(request=request_model)
