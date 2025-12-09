from datetime import datetime
from typing import List

from nisystemlink.clients.core._uplink._with_paging import WithPaging
from pydantic import StrictBool, StrictInt

from ._order_by import OrderBy


class QueryTablesRequest(WithPaging):
    """Request parameters for querying tables."""

    filter: str
    """The table query filter in `Dynamic LINQ`_ format.

    .. _Dynamic LINQ: https://github.com/ni/systemlink-OpenAPI-documents/wiki/Dynamic-Linq-Query-Language

    Allowed properties in the filter are:

    * ``columns``: List of columns in the table (see below; requires version 2 of the
      :py:attr:`nisystemlink.clients.dataframe.models.OperationsV1.list_tables` operation)
    * ``createdAt``: DateTime the table was created
    * ``createdWithin``: TimeSpan in which the table was created
    * ``id``: String value uniquely identifying the table
    * ``name``: String name for the table
    * ``metadataModifiedAt``: DateTime the table's metadata was last modified
    * ``metadataModifiedWithin``: TimeSpan in which the table's metadata was
      last modified
    * ``properties``: Dictionary with string keys and values representing table
      metadata
    * ``rowsModifiedAt``: DateTime rows were last appended to the table
    * ``rowsModifiedWithin``: TimeSpan within rows were last appended to the
      table
    * ``rowCount``: Int32 number of rows in the table
    * ``supportsAppend``: Boolean indicating whether or not the table supports
      appending additional rows of data
    * ``testResultId``: String ID of the test result associated with the table (requires version 2
      of the :py:attr:`nisystemlink.clients.dataframe.models.OperationsV1.list_tables` operation)
    * ``workspace``: String ID of the workspace the table belongs to
    * ``workspaceName``: String name of the workspace the table belongs to

    Allowed properties in the ``columns`` list are:

    * ``name``: String name of the column (requires a ``testResultId`` filter)

    Allowed constants in the filter are:

    * ``RelativeTime.CurrentDay``: TimeSpan representing the elapsed time
      between now and the start of the current day
    * ``RelativeTime.CurrentWeek``: TimeSpan representing the elapsed time
      between now and the start of the current week
    * ``RelativeTime.CurrentMonth``: TimeSpan representing the elapsed time
      between now and the start of the current month
    * ``RelativeTime.CurrentYear``: TimeSpan representing the elapsed time
      between now and the start of the current year
    """

    substitutions: List[StrictInt | StrictBool | str | None] | None = None
    """Make substitutions in the query filter expression.

    Substitutions for the query expression are indicated by non-negative
    integers that are prefixed with the ``@`` symbol. Each substitution in the given
    expression will be replaced by the element at the corresponding index
    (zero-based) in this list. For example, ``@0`` in the filter expression will be
    replaced with the element at the zeroth index of the substitutions list.
    """

    reference_time: datetime | None = None
    """The date and time to use as the reference point for `RelativeTime` filters,
    including time zone information. Defaults to the time on the server in UTC."""

    take: int | None = None
    """Limits the returned list to the specified number of results."""

    order_by: OrderBy | None = None
    """The sort order of the returned list of tables."""

    order_by_descending: bool | None = None
    """Whether to sort descending instead of ascending.

    The elements in the list are sorted ascending by default. If the
    orderByDescending parameter is specified, the elements in the list are
    sorted based on it's value. The orderByDescending value must be a boolean
    string. The elements in the list are sorted ascending if false and
    descending if true.
    """

    interactive: bool | None = None
    """Whether the query is being made within an interactive context, such as a web UI.
    Interactive queries receive faster feedback for slow queries. Added in version 2 of the
    :py:attr:`nisystemlink.clients.dataframe.models.OperationsV1.list_tables` operation.
    Older versions of the service will ignore this value."""
