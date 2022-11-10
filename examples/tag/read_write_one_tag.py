from datetime import timedelta

from nisystemlink.clients.tag import DataType, TagManager

mgr = TagManager()
tag = mgr.open("MyTags.Example Tag", DataType.DOUBLE, create=True)

with mgr.create_writer(buffer_size=10, max_buffer_time=timedelta(seconds=3)) as writer:
    writer.write(tag.path, tag.data_type, 3.5)
# Note: Exiting the "with" block automatically calls writer.send_buffered_writes()

read_result = mgr.read(tag.path)
assert read_result is not None
assert read_result.value == 3.5
