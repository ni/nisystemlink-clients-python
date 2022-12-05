from typing import Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._data_frame import DataFrame


class AppendTableDataRequest(JsonModel):
    """Contains the rows to append and optional flags. The ``frame`` field is
    required unless ``endOfData`` is true.
    """

    frame: Optional[DataFrame] = None
    """The data frame containing the rows to append."""

    end_of_data: Optional[bool] = None
    """Whether the table should expect any additional rows to be appended in future requests."""
