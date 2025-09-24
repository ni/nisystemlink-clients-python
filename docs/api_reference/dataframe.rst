.. _api_tag_page:

nisystemlink.clients.dataframe
======================

.. autoclass:: nisystemlink.clients.dataframe.DataFrameClient
   :exclude-members: __init__

   .. automethod:: __init__
   .. automethod:: api_info
   .. automethod:: list_tables
   .. automethod:: create_table
   .. automethod:: query_tables
   .. automethod:: get_table_metadata
   .. automethod:: modify_table
   .. automethod:: delete_table
   .. automethod:: delete_tables
   .. automethod:: modify_tables
   .. automethod:: get_table_data
   .. automethod:: append_table_data
   .. automethod:: query_table_data
   .. automethod:: export_table_data
   .. automethod:: query_decimated_data

.. automodule:: nisystemlink.clients.dataframe.models
   :members:
   :imported-members:

Arrow / JSON Ingestion Notes
----------------------------
``append_table_data`` accepts multiple data forms:

* ``AppendTableDataRequest`` (JSON)
* ``DataFrame`` model (JSON)
* Single ``pyarrow.RecordBatch`` (Arrow IPC)
* Iterable of ``pyarrow.RecordBatch`` (Arrow IPC)
* ``None`` with ``end_of_data`` (flush only)

Arrow support is optional and requires installing the ``pyarrow`` extra::

   pip install "nisystemlink-clients[pyarrow]"

If ``pyarrow`` is not installed and a RecordBatch (or iterable) is passed, a
``RuntimeError`` is raised. When Arrow is used, the batches are serialized into
an IPC stream and sent with content type
``application/vnd.apache.arrow.stream``; the ``end_of_data`` flag is sent as a
query parameter. JSON ingestion places ``endOfData`` in the request body.

If the target SystemLink DataFrame Service does not yet support Arrow and
responds with HTTP 400, the client raises an explanatory ``ApiException``
advising to upgrade or fall back to JSON ingestion.
