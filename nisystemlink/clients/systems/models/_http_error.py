from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class HttpError(JsonModel):
    """Represents the standard error structure."""

    name: Optional[str] = None
    """Gets the fully-qualified name that identifies the error code, such as the output of M:NationalInstruments.SystemLink.ServiceBase.ErrorHandling.ErrorCode.ToString."""

    code: Optional[int] = None
    """Gets the optional NationalInstruments.SystemLink.ServiceBase.ErrorHandling.ErrorCode.NumericCode (not HTTP status code) that identifies the error code."""

    message: Optional[str] = None
    """Gets the formatted error message, which is the NationalInstruments.SystemLink.ServiceBase.ErrorHandling.ErrorCode.Message with NationalInstruments.SystemLink.ServiceBase.HttpError.Args inserted into any placeholders."""

    resourceType: Optional[str] = None
    """Gets the type of resource associated with the error, if any. Typically only used for instances within NationalInstruments.SystemLink.ServiceBase.HttpError.InnerErrors."""

    resourceId: Optional[str] = None
    """Gets the ID of the resource associated with the error, if any. Typically only used for instances within NationalInstruments.SystemLink.ServiceBase.HttpError.InnerErrors."""

    args: Optional[List[str]] = None
    """Gets the arguments that produced NationalInstruments.SystemLink.ServiceBase.HttpError.Message."""

    innerErrors: Optional[List["HttpError"]] = None
    """Gets any nested errors if this instance represents more than one error. Typically only set for instances related to NationalInstruments.SystemLink.ServiceBase.ErrorHandling.SkylineErrorCodes.OneOrMoreErrorsOccurred."""
