from typing import List, Optional

from nisystemlink.clients.core._uplink._with_paging import WithPaging

from ._notebook_metadata import NotebookMetadata


class PagedNotebooks(WithPaging):
    """Model for a query notebooks response."""

    notebooks: Optional[List[NotebookMetadata]] = None
    """The list of notebooks."""
