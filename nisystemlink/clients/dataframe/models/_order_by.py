from typing import Literal

# TODO: Migrate to Enum when this change is released: https://github.com/prkumar/uplink/pull/282
OrderBy = Literal[
    "CREATED_AT", "METADATA_MODIFIED_AT", "NAME", "NUMBER_OF_ROWS", "ROWS_MODIFIED_AT"
]
"""Possible options for sorting when querying tables.

* ``CREATED_AT``: The date and time the table was created.
* ``METADATA_MODIFIED_AT``: The date and time the table's metadata properties were modified.
* ``NAME``: The name of the table.
* ``NUMBER_OF_ROWS``: The number of rows of data in the table.
* ``ROWS_MODIFIED_AT``: Date and time rows were most recently appended to the table.
"""
