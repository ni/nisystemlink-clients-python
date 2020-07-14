from contextlib import ExitStack
from time import sleep

from systemlink.clients.tag import DataType, TagData, TagManager, TagValueReader

SIMULATE_EXTERNAL_TAG_CHANGES = True


def on_tag_changed(tag: TagData, reader: TagValueReader) -> None:
    """Callback for tag_changed events."""
    path = tag.path
    data_type = tag.data_type.name

    if reader is not None:
        read_result = reader.read()
        # A read_result of None means that the tag has no value, but it *must*
        # have a value, because we got a tag_changed event!
        assert read_result is not None
        value = read_result.value
    else:
        value = "???"  # tag has unknown data type

    print(f'Tag changed: "{path}" = {value} ({data_type})')


mgr = TagManager()
if SIMULATE_EXTERNAL_TAG_CHANGES:
    mgr.open("MyTags.Example Tag", DataType.DOUBLE, create=True)
    writer = mgr.create_writer(buffer_size=1)

with ExitStack() as stack:
    # Notes:
    # 1. The tags are assumed to already exist before this example is run, but
    #    setting SIMULATE_EXTERNAL_TAG_CHANGES to True will ensure there is one.
    # 2. Any tags that get added later will NOT automatically appear in the
    #    selection just because the path matches the wildcard used below; you
    #    must call one of the selection's refresh methods to update the tag list
    #    from the server. But even if you do that:
    # 3. The subscription will only contain the tags that were in the selection
    #    when the subscription was created. If you want the subscription to add
    #    new tags that were added to the selection, you must recreate it.
    paths = ["MyTags.*"]
    selection = stack.enter_context(mgr.open_selection(paths))
    if not selection.metadata:
        print(f"Found no tags that match {paths}")
    else:
        print("Matching tags:")
        for path in selection.metadata.keys():
            print(f" - {path}")
        print()

        subscription = stack.enter_context(selection.create_subscription())
        subscription.tag_changed += on_tag_changed

        # Wait forever, until a KeyboardInterrupt (Ctrl+C)
        print("Watching for tag changes; hit Ctrl+C to stop")
        try:
            i = 0
            while True:
                sleep(1)
                if SIMULATE_EXTERNAL_TAG_CHANGES:
                    writer.write("MyTags.Example Tag", DataType.DOUBLE, i)
                    i += 1
        except KeyboardInterrupt:
            pass
