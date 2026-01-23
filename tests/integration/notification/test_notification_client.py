import pytest
from nisystemlink.clients.core import ApiException
from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.notification import NotificationClient
from nisystemlink.clients.notification.models import (
    AddressFields,
    AddressGroup,
    DynamicNotificationConfiguration,
    DynamicNotificationStrategy,
    DynamicStrategyRequest,
    MessageTemplate,
    MessageTemplateFields,
)


@pytest.fixture
def request_model():
    """Returns the created request."""
    _address_group = AddressGroup(
        id="address_group_id",
        interpreting_service_name="smtp",
        display_name="name",
        properties={"property": "value"},
        fields=AddressFields(
            toAddresses=["address1@example.com"],
            ccAddresses=["address2@example.com"],
            bccAddresses=["address3@example.com"],
        ),
        referencing_notification_strategies=["reference_notification_strategy"],
    )
    _message_template = MessageTemplate(
        id="message_group_id",
        interpreting_service_name="smtp",
        display_name="name",
        properties={"property": "value"},
        fields=MessageTemplateFields(subject_template="subject", body_template="body"),
        referencing_notification_strategies=["reference_notification_strategy"],
    )
    _notification_configuration = DynamicNotificationConfiguration(
        address_group_id="address_group_id",
        message_template_id="message_group_id",
        address_group=_address_group,
        message_template=_message_template,
    )

    _notification_strategy = DynamicNotificationStrategy(
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

    def test__apply_strategy_with_invalid_recipient__raises_exception(
        self, client: NotificationClient, request_model: DynamicStrategyRequest
    ):
        address_group = request_model.notification_strategy.notification_configurations[
            0
        ].address_group

        assert address_group is not None
        address_group.fields = AddressFields(toAddresses=["invalid-email"])

        with pytest.raises(ApiException):
            client.apply_notification_strategy(request=request_model)

    def test__apply_strategy_with_no_configurations__raises_exception(
        self, client: NotificationClient, request_model: DynamicStrategyRequest
    ):
        request_model.notification_strategy.notification_configurations = []

        with pytest.raises(ApiException):
            client.apply_notification_strategy(request=request_model)

    def test__apply_strategy_with_empty_subject_template_fields__raises_exception(
        self, client: NotificationClient, request_model: DynamicStrategyRequest
    ):
        message_template = (
            request_model.notification_strategy.notification_configurations[
                0
            ].message_template
        )
        assert message_template is not None
        message_template.fields.subject_template = ""

        with pytest.raises(ApiException):
            client.apply_notification_strategy(request=request_model)

    def test__apply_strategy_with_invalid_interpreting_service_name__raises_exception(
        self, client: NotificationClient, request_model: DynamicStrategyRequest
    ):
        address_group = request_model.notification_strategy.notification_configurations[
            0
        ].address_group
        assert address_group is not None
        address_group.interpreting_service_name = ""

        with pytest.raises(ApiException):
            client.apply_notification_strategy(request=request_model)

    def test__apply_configuration_with_no_address_and_message_template_id__returns_none(
        self, client: NotificationClient, request_model: DynamicStrategyRequest
    ):
        temp_request = request_model

        configuration = DynamicNotificationConfiguration(
            address_group=request_model.notification_strategy.notification_configurations[
                0
            ].address_group,
            message_template=request_model.notification_strategy.notification_configurations[
                0
            ].message_template,
        )

        temp_request = DynamicStrategyRequest(
            message_template_substitution_fields=request_model.message_template_substitution_fields,
            notification_strategy=DynamicNotificationStrategy(
                notification_configurations=[configuration]
            ),
        )
        assert client.apply_notification_strategy(request=temp_request) is None
