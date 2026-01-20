from copy import deepcopy

import pytest

from nisystemlink.clients.core import ApiException
from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.notification import NotificationClient
from nisystemlink.clients.notification.models import (
    AddressGroup,
    DynamicStrategyRequest,
    MessageTemplate,
    NotificationConfiguration,
    NotificationStrategy,
)


class GenerateRequest:
    """Creates a sample valid request for the notification client."""

    _address_group = AddressGroup(
        id="address_group_id",
        interpreting_service_name="smtp",
        display_name="name",
        properties={"property": "value"},
        fields={
            "toAddresses": ["address1@example.com"],
        },
        referencing_notification_strategies=["reference_notification_strategy"],
    )

    _message_template = MessageTemplate(
        id="address_group_id",
        interpreting_service_name="smtp",
        display_name="name",
        properties={"property": "value"},
        fields={
            "subjectTemplate": "subject",
            "bodyTemplate": "body",
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

    @classmethod
    def getRequestBody(self):
        """Returns the created request."""
        return self._dynamic_strategy_request


@pytest.fixture
def client(enterprise_config: HttpConfiguration) -> NotificationClient:
    """Fixture to create a Notification client."""
    return NotificationClient(enterprise_config)


@pytest.mark.integration
@pytest.mark.enterprise
class TestNotificationClient:
    request = GenerateRequest.getRequestBody()

    def test__apply_strategy_with_correct_request__returns_none(
        self, client: NotificationClient
    ):
        assert client.apply_notification_strategy(request=self.request) is None

    def test__apply_strategy_with_empty_template_substitution_fields__raises_exception(
        self, client: NotificationClient
    ):
        fetched_request = deepcopy(self.request)
        fetched_request.message_template_substitution_fields = None

        with pytest.raises(ApiException):
            client.apply_notification_strategy(request=fetched_request)

    def test__apply_strategy_with_no_recipient__raises_exception(
        self, client: NotificationClient
    ):
        fetched_request = deepcopy(self.request)
        fetched_request.notification_strategy.notification_configurations[
            0
        ].address_group.fields = {}

        with pytest.raises(ApiException):
            client.apply_notification_strategy(request=fetched_request)

    def test__apply_strategy_with_invalid_recipient__raises_exception(
        self, client: NotificationClient
    ):
        fetched_request = deepcopy(self.request)
        fetched_request.notification_strategy.notification_configurations[
            0
        ].address_group.fields = {"toAddresses": ["sample"]}

        with pytest.raises(ApiException):
            client.apply_notification_strategy(request=fetched_request)

    def test__apply_strategy_with_no_configurations__raises_exception(
        self, client: NotificationClient
    ):
        fetched_request = deepcopy(self.request)
        fetched_request.notification_strategy.notification_configurations = []

        with pytest.raises(ApiException):
            client.apply_notification_strategy(request=fetched_request)

    def test__apply_strategy_with_empty_address_groups__raises_exception(
        self, client: NotificationClient
    ):
        fetched_request = deepcopy(self.request)
        fetched_request.notification_strategy.notification_configurations[
            0
        ].address_group = None

        with pytest.raises(ApiException):
            client.apply_notification_strategy(request=fetched_request)

    def test__apply_strategy_with_empty_message_template__raises_exception(
        self, client: NotificationClient
    ):
        fetched_request = deepcopy(self.request)
        fetched_request.notification_strategy.notification_configurations[
            0
        ].message_template = None

        with pytest.raises(ApiException):
            client.apply_notification_strategy(request=fetched_request)

    def test__apply_strategy_with_invalid_message_template_fields__raises_exception(
        self, client: NotificationClient
    ):
        fetched_request = deepcopy(self.request)
        fetched_request.notification_strategy.notification_configurations[
            0
        ].message_template.fields = {"bodyTemplate": "body"}

        with pytest.raises(ApiException):
            client.apply_notification_strategy(request=fetched_request)
