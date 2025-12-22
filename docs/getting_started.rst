.. _getting_started:

Getting Started
===============

Alarm API
---------

Overview
~~~~~~~~

The :class:`.AlarmClient` class is the primary entry point of the Alarm API.

When constructing an :class:`.AlarmClient`, you can pass an
:class:`.HttpConfiguration` (like one retrieved from the
:class:`.HttpConfigurationManager`), or let :class:`.AlarmClient` use the
default connection. The default connection depends on your environment.

With an :class:`.AlarmClient` object, you can:

* Create and update alarm instances using :meth:`~.AlarmClient.create_or_update_alarm`

  * Alarms have two key identifiers:
  
    * ``alarm_id``: A user-defined identifier for the alarm type
    * ``instance_id``: A server-generated unique identifier for each alarm occurrence
  
  * Create alarm transitions (SET, CLEAR) to track alarm state changes

* Query alarms with :meth:`~.AlarmClient.query_alarms`

  * Filter alarms using Dynamic LINQ expressions
  * Control which transitions are returned (most recent only or all)
  * Sort and paginate results

* Get a specific alarm by its instance_id using :meth:`~.AlarmClient.get_alarm`

* Acknowledge alarms by its instance_id using :meth:`~.AlarmClient.acknowledge_alarms`

  * Optionally force-clear alarms when acknowledging

* Delete alarms using :meth:`~.AlarmClient.delete_alarm` or 
  :meth:`~.AlarmClient.delete_alarms`

Examples
~~~~~~~~

Create, query, acknowledge, and delete alarms

.. literalinclude:: ../examples/alarm/alarm.py
   :language: python
   :linenos:


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


Product API
-------

Overview
~~~~~~~~

The :class:`.ProductClient` class is the primary entry point of the Product API.

When constructing a :class:`.ProductClient`, you can pass an
:class:`.HttpConfiguration` (like one retrieved from the
:class:`.HttpConfigurationManager`), or let :class:`.ProductClient` use the
default connection. The default connection depends on your environment.

With a :class:`.ProductClient` object, you can:

* Create, update, query, and delete Products

Examples
~~~~~~~~

Create, query, update, and delete some products

.. literalinclude:: ../examples/product/products.py
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

Spec API
-------

Overview
~~~~~~~~


The :class:`.SpecClient` class is the primary entry point of the Specification Compliance API.

When constructing a :class:`.SpecClient`, you can pass an
:class:`.HttpConfiguration` (like one retrieved from the
:class:`.HttpConfigurationManager`), or let :class:`.SpecClient` use the
default connection. The default connection depends on your environment.

With a :class:`.SpecClient` object, you can: 

* Create and delete specifications under a product.

* Modify any fields of an existing specification

* Query for specifications on any fields using DynamicLinq syntax.

* Get a specification using an Id.

Examples
~~~~~~~~

Create, Get and Query Specifications

.. literalinclude:: ../examples/spec/get_and_query_specs.py
   :language: python
   :linenos:

Update and Delete Specifications

.. literalinclude:: ../examples/spec/update_and_delete_specs.py
   :language: python
   :linenos:


File API
-------

Overview
~~~~~~~~

The :class:`.FileClient` class is the primary entry point of the File API.

When constructing a :class:`.FileClient`, you can pass an
:class:`.HttpConfiguration` (like one retrieved from the
:class:`.HttpConfigurationManager`), or let :class:`.FileClient` use the
default connection. The default connection depends on your environment.

With a :class:`.FileClient` object, you can:

* Get the list of files, download and delete files

Examples
~~~~~~~~

Get the metadata of a File using its Id and download it.

.. literalinclude:: ../examples/file/download_file.py
   :language: python
   :linenos:

Upload a File from disk or memory to SystemLink

.. literalinclude:: ../examples/file/upload_file.py

Feeds API
-------

Overview
~~~~~~~~

The :class:`.FeedsClient` class is the primary entry point of the Feeds API.

When constructing a :class:`.FeedsClient`, you can pass an
:class:`.HttpConfiguration` (like one retrieved from the
:class:`.HttpConfigurationManager`), or let :class:`.FeedsClient` use the
default connection. The default connection depends on your environment.

With a :class:`.FeedsClient` object, you can:

* Get the list of feeds, create feed, upload package to feed and delete feed.

Examples
~~~~~~~~

Create a new feed.

.. literalinclude:: ../examples/feeds/create_feed.py
   :language: python
   :linenos:

Query feeds and upload a package to feed.

.. literalinclude:: ../examples/feeds/query_and_upload_feeds.py
   :language: python
   :linenos:

Delete a feed.

.. literalinclude:: ../examples/feeds/delete_feed.py
   :language: python
   :linenos:

TestMonitor API (Results and Steps)
-------

Overview
~~~~~~~~

The :class:`.TestMonitorClient` class is the primary entry point of the Test Monitor API
used to interact with test results (Results) and test steps (Steps).

When constructing a :class:`.TestMonitorClient`, you can pass an
:class:`.HttpConfiguration` (like one retrieved from the
:class:`.HttpConfigurationManager`), or let :class:`.TestMonitorClient` use the
default connection. The default connection depends on your environment.

With a :class:`.TestMonitorClient` object, you can:

* Create, update, query, and delete results
* Create, update, query, and delete steps

Examples
~~~~~~~~

Create, query, update, and delete some results

.. literalinclude:: ../examples/testmonitor/results.py
   :language: python
   :linenos:

Create, update, query, and delete steps

.. literalinclude:: ../examples/testmonitor/steps.py
   :language: python
   :linenos:

Notebook API
-------

Overview
~~~~~~~~

The :class:`.NotebookClient` class is the primary entry point of the Notebook API.

When constructing a :class:`.NotebookClient`, you can pass an
:class:`.HttpConfiguration` (like one retrieved from the
:class:`.HttpConfigurationManager`), or let :class:`.NotebookClient` use the
default connection. The default connection depends on your environment.

With a :class:`.NotebookClient` object, you can:

* Create, update, query, and delete Notebooks
* Create, get and query Notebook Executions

Examples
~~~~~~~~

Create, query, update, and delete some notebooks.

.. literalinclude:: ../examples/notebook/notebook.py
   :language: python
   :linenos:

Create, query, retry, and cancel notebook executions.

.. literalinclude:: ../examples/notebook/notebook_execution.py
   :language: python
   :linenos:

Asset Management API
-------

Overview
~~~~~~~~

The :class:`.AssetManagementClient` class is the primary entry point of the Asset Management API.

When constructing a :class:`.AssetManagementClient`, you can pass an
:class:`.HttpConfiguration` (like one retrieved from the
:class:`.HttpConfigurationManager`), or let :class:`.AssetManagementClient` use the
default connection. The default connection depends on your environment.

With a :class:`.AssetManagementClient` object, you can:

* Create, delete, get the list of assets and link files to assets.

Examples
~~~~~~~~

create, delete, query asset and link files to assets.

.. literalinclude:: ../examples/assetmanagement/assets.py
   :language: python
   :linenos:

Systems API
-------

Overview
~~~~~~~~

The :class:`.SystemsClient` class is the primary entry point of the Systems API.

When constructing a :class:`.SystemsClient`, you can pass an
:class:`.HttpConfiguration` (like one retrieved from the
:class:`.HttpConfigurationManager`), or let :class:`.SystemsClient` use the
default connection. The default connection depends on your environment.

With a :class:`.SystemsClient` object, you can:

* Create, query, and remove systems.

Examples
~~~~~~~~

Create, query, and remove some systems.

.. literalinclude:: ../examples/systems/systems.py
   :language: python
   :linenos:

TestPlan API
-------

Overview
~~~~~~~~

The :class:`.TestPlanClient` class is the primary entry point of the TestPlan API.

When constructing a :class:`.TestPlanClient`, you can pass an
:class:`.HttpConfiguration` (like one retrieved from the
:class:`.HttpConfigurationManager`), or let :class:`.TestPlanClient` use the
default connection. The default connection depends on your environment.

With a :class:`.TestPlanClient` object, you can:

* Create, query, get, update, schedule and delete TestPlans
* Create, query and delete test plan templates

Examples
~~~~~~~~

Create, query, get, update, schedule and delete TestPlans

.. literalinclude:: ../examples/test_plan/test_plans.py
   :language: python
   :linenos:

Create, query and delete test plan templates.

.. literalinclude:: ../examples/test_plan/test_plan_templates.py
   :language: python
   :linenos:
