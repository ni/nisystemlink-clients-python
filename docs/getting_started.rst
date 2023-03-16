.. _getting_started:

Getting Started
===============

Tag API
-------

Overview
~~~~~~~~

The :class:`.TagManager` class is the primary entry point of the Tag API.

When constructing a :class:`.TagManager`, you can pass an
:class:`.HttpConfiguration` (like one retrieved from the
:class:`.HttpConfigurationManager`), or let :class:`.TagManager` use the
default connection. The default connection depends on your SystemLink Client
settings.

With a :class:`.TagManager` object, you can:

* Query, create, modify, and delete tags from the server

  * Use :meth:`~.TagManager.open()` to get a tag's :class:`.TagData` from the
    server when you know the tag's ``path``.
  * Use :meth:`~.TagManager.query()` to get a :class:`collection
    <.TagQueryResultCollection>` of :class:`.TagData` objects based on the
    tags' ``paths``, ``keywords``, and/or ``properties``.
  * Use :meth:`~.TagManager.refresh()` to update a list of :class:`.TagData`
    objects with fresh metadata from the server.
  * Use :meth:`~.TagManager.update()` to modify the server metadata for a list
    of tags, using either :class:`.TagData` objects to overwrite the server's
    tag data or :class:`.TagDataUpdate` objects to selectively update specific
    fields.
  * Use :meth:`~.TagManager.delete()` to delete one or more tags from the
    server.

* Read and write tag values

  * Use :meth:`~.TagManager.read()` to get a tag's current value. Via method
    parameters, you can also request the timestamp indicating when that value
    was last written and/or the aggregate data stored for the tag (if the tag's
    :attr:`~.TagData.collect_aggregates` attribute is enabled on the server).
  * Use :meth:`~.TagManager.create_writer()` to get a
    :class:`.BufferedTagWriter` that will buffer a set of writes, and
    automatically send the writes when a given ``buffer_size`` is reached or
    when ``max_buffer_time`` has elapsed (or when
    :meth:`~.BufferedTagWriter.send_buffered_writes()` is called).

* Get a :class:`.TagSelection` that can help perform several of the above
  operations on several tags at once

  * Use :meth:`.TagManager.create_selection` if you already have a list of
    :class:`.TagData` objects that you want to perform a set of operations on.
  * Use :meth:`.TagManager.open_selection` if you just have a list of ``paths``
    -- optionally including glob-style wildcards! -- with which to create the
    selection.

If you have a :class:`.TagSelection`, you can use it to :meth:`create
<.TagSelection.create_subscription>` a :class:`.TagSubscription` that will
trigger a :attr:`~.TagSubscription.tag_changed` event any time one of the tags'
values is changed.

Examples
~~~~~~~~

Read and write individual tags

.. literalinclude:: ../examples/tag/read_write_one_tag.py
   :language: python
   :linenos:

Subscribe to tag changes

.. literalinclude:: ../examples/tag/subscribe_to_tag_changes.py
   :language: python
   :linenos:

DataFrame API
-------

Overview
~~~~~~~~

The :class:`.DataFrameClient` class is the primary entry point of the DataFrame API.

When constructing a :class:`.DataFrameClient`, you can pass an
:class:`.HttpConfiguration` (like one retrieved from the
:class:`.HttpConfigurationManager`), or let :class:`.DataFrameClient` use the
default connection. The default connection depends on your environment.

With a :class:`.DataFrameClient` object, you can:

* Create and delete data tables.

* Modify table metadata and query for tables by their metadata.

* Append rows of data to a table, query for rows of data from a table, and
  decimate table data.

* Export table data in a comma-separated values (CSV) format.

Examples
~~~~~~~~

Create and write data to a table

.. literalinclude:: ../examples/dataframe/create_write_data.py
   :language: python
   :linenos:

Query and read data from a table

.. literalinclude:: ../examples/dataframe/query_read_data.py
   :language: python
   :linenos:

Export data from a table
.. literalinclude:: ../examples/dataframe/export_data.py
   :language: python
   :linenos: