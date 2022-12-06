from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._data_frame import DataFrame


class TableRows(JsonModel):
    """Contains the result of a query for rows of decimated data."""

    frame: DataFrame
    """The data frame containing the rows of data."""
