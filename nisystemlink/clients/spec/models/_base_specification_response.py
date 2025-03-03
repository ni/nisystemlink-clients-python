from nisystemlink.clients.core._uplink._json_model import JsonModel


class BaseSpecificationResponse(JsonModel):
    """Base Response Model for create specs response and update specs response."""

    id: str
    """The global Id of the specification."""

    version: int
    """
    Current version of the specification.

    When an update is applied, the version is automatically incremented.
    """

    product_id: str
    """Id of the product to which the specification will be associated."""

    spec_id: str
    """User provided value using which the specification will be identified.

    This should be unique for a product and workspace combination.
    """
