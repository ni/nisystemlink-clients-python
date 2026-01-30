import pytest
import responses
from nisystemlink.clients.core import ApiException
from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.notification import NotificationClient
from nisystemlink.clients.notification.models import (
    DynamicNotificationConfiguration,
    DynamicNotificationStrategy,
    DynamicStrategyRequest,
    SmtpAddressFields,
    SmtpAddressGroup,
    SmtpMessageTemplate,
    SmtpMessageTemplateFields,
)
from pydantic import ValidationError

BASE_URL = "https://test-api.lifecyclesolutions.ni.com"


@pytest.fixture
def _smtp_address_group():
    """Returns the created address group."""
    return SmtpAddressGroup(
        id="address_group_id",
        interpreting_service_name="smtp",
        display_name="name",
        properties={"property": "value"},
        fields=SmtpAddressFields(
            toAddresses=["address1@example.com"],
            ccAddresses=["address2@example.com"],
            bccAddresses=["address3@example.com"],
        ),
        referencing_notification_strategies=["reference_notification_strategy"],
    )


@pytest.fixture
def _smtp_message_template():
    """Returns the created message template."""
    return SmtpMessageTemplate(
        id="message_template_id",
        interpreting_service_name="smtp",
        display_name="name",
        properties={"property": "value"},
        fields=SmtpMessageTemplateFields(
            subject_template="subject", body_template="body"
        ),
        referencing_notification_strategies=["reference_notification_strategy"],
    )


@pytest.fixture
def _notification_configuration(
    _smtp_address_group: SmtpAddressGroup, _smtp_message_template: SmtpMessageTemplate
):
    """Returns the created notification configuration."""
    return DynamicNotificationConfiguration(
        address_group_id="address_group_id",
        message_template_id="message_template_id",
        address_group=_smtp_address_group,
        message_template=_smtp_message_template,
    )


@pytest.fixture
def _notification_strategy(
    _notification_configuration: DynamicNotificationConfiguration,
):
    """Returns the created notification strategy."""
    return DynamicNotificationStrategy(
        notification_configurations=[
            _notification_configuration,
        ]
    )


@pytest.fixture
def request_model(
    _notification_strategy: DynamicNotificationStrategy,
):
    """Returns the created request."""
    return DynamicStrategyRequest(
        message_template_substitution_fields={"replacement": "value"},
        notification_strategy=_notification_strategy,
    )


@pytest.fixture(scope="class")
def client(enterprise_config: HttpConfiguration) -> NotificationClient:
    """Fixture to create a Notification client."""
    return NotificationClient(enterprise_config)


@pytest.mark.integration
@pytest.mark.enterprise
class TestNotificationClient:
    @responses.activate
    def test__apply_strategy_with_correct_request__returns_none(
        self, client: NotificationClient, request_model: DynamicStrategyRequest
    ):
        responses.add(
            responses.POST,
            f"{BASE_URL}/ninotification/v1/apply-dynamic-strategy",
            status=204,
        )
        assert client.apply_dynamic_notification_strategy(request=request_model) is None

    def test__apply_strategy_with_invalid_recipient_for_smtp_service__raises_exception(
        self,
        client: NotificationClient,
        _smtp_message_template: SmtpMessageTemplate,
    ):
        address_group = SmtpAddressGroup(
            interpreting_service_name="smtp",
            fields=SmtpAddressFields(toAddresses=["invalid-email"]),
        )

        request_model = DynamicStrategyRequest(
            message_template_substitution_fields={"replacement": "value"},
            notification_strategy=DynamicNotificationStrategy(
                notification_configurations=[
                    DynamicNotificationConfiguration(
                        address_group=address_group,
                        message_template=_smtp_message_template,
                    )
                ]
            ),
        )

        with pytest.raises(ApiException, match="Bad Request") as exc_info:
            client.apply_dynamic_notification_strategy(request=request_model)

        assert exc_info.value.http_status_code == 400

    def test__create_strategy_with_no_configurations__raises_exception(self):
        with pytest.raises(ValidationError):
            DynamicStrategyRequest(
                message_template_substitution_fields={"replacement": "value"},
                notification_strategy=DynamicNotificationStrategy(
                    notification_configurations=[]
                ),
            )

    def test__apply_strategy_with_empty_subject_for_smtp_message_template__raises_exception(
        self, client: NotificationClient, _smtp_address_group: SmtpAddressGroup
    ):
        message_template = SmtpMessageTemplate(
            interpreting_service_name="smtp",
            fields=SmtpMessageTemplateFields(subject_template=""),
        )

        request_model = DynamicStrategyRequest(
            message_template_substitution_fields={"replacement": "value"},
            notification_strategy=DynamicNotificationStrategy(
                notification_configurations=[
                    DynamicNotificationConfiguration(
                        address_group=_smtp_address_group,
                        message_template=message_template,
                    )
                ]
            ),
        )

        with pytest.raises(ApiException, match="Bad Request") as exc_info:
            client.apply_dynamic_notification_strategy(request=request_model)

        assert exc_info.value.http_status_code == 400

    def test__create_address_group_with_invalid_interpreting_service_name__raises_exception(
        self,
    ):
        with pytest.raises(ValidationError):
            SmtpAddressGroup(
                interpreting_service_name="invalid_service",
                fields=SmtpAddressFields(toAddresses=["address1@example.com"]),
            )

    @responses.activate
    def test__apply_strategy_with_no_address_group_id_and_message_template_id__returns_none(
        self,
        client: NotificationClient,
        _smtp_address_group: SmtpAddressGroup,
        _smtp_message_template: SmtpMessageTemplate,
    ):
        responses.add(
            responses.POST,
            f"{BASE_URL}/ninotification/v1/apply-dynamic-strategy",
            status=204,
        )
        configuration = DynamicNotificationConfiguration(
            address_group=_smtp_address_group,
            message_template=_smtp_message_template,
        )

        request_model = DynamicStrategyRequest(
            message_template_substitution_fields={"replacement": "value"},
            notification_strategy=DynamicNotificationStrategy(
                notification_configurations=[
                    configuration,
                ]
            ),
        )
        assert client.apply_dynamic_notification_strategy(request=request_model) is None

    @responses.activate
    def test__apply_multiple_notification_configurations__returns_none(
        self,
        client: NotificationClient,
        _smtp_address_group: SmtpAddressGroup,
    ):
        responses.add(
            responses.POST,
            f"{BASE_URL}/ninotification/v1/apply-dynamic-strategy",
            status=204,
        )
        first_message_template = SmtpMessageTemplate(
            interpreting_service_name="smtp",
            fields=SmtpMessageTemplateFields(
                subject_template="subject1", body_template="body1"
            ),
        )
        second_message_template = SmtpMessageTemplate(
            interpreting_service_name="smtp",
            fields=SmtpMessageTemplateFields(
                subject_template="subject2", body_template="body2"
            ),
        )

        configuration1 = DynamicNotificationConfiguration(
            address_group=_smtp_address_group,
            message_template=first_message_template,
        )

        configuration2 = DynamicNotificationConfiguration(
            address_group=_smtp_address_group,
            message_template=second_message_template,
        )

        request_model = DynamicStrategyRequest(
            message_template_substitution_fields={"replacement": "value"},
            notification_strategy=DynamicNotificationStrategy(
                notification_configurations=[
                    configuration1,
                    configuration2,
                ]
            ),
        )
        assert client.apply_dynamic_notification_strategy(request=request_model) is None
