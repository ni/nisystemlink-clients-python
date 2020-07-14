import datetime
import os
import threading
import time

from systemlink.clients.tag._core._system_time_stamper import SystemTimeStamper


class TestSystemTimeStamper:
    def test__constructed__returns_current_time(self):
        uut = SystemTimeStamper()
        _assert_time_within_tolerance(_gmt_now(), uut.timestamp)

    def test__after_delay__returns_current_time(self):
        uut = SystemTimeStamper()
        _assert_time_within_tolerance(_gmt_now(), uut.timestamp)
        time.sleep(0.05)
        _assert_time_within_tolerance(_gmt_now(), uut.timestamp)

    def test__during_heavy_use__prevents_collisions(self):
        uut = SystemTimeStamper()
        times = []
        num_times = 500

        def worker():
            while len(times) < num_times:
                times.append(uut.timestamp)

        num_threads = max(os.cpu_count(), 4)
        threads = [threading.Thread(target=worker) for i in range(num_threads)]
        begin = _gmt_now()
        [t.start() for t in threads]
        [t.join() for t in threads]

        times.sort()

        num_after_1us = 0
        for i, t in enumerate(times):
            _assert_time_within_tolerance(begin, t)

            if i > 0:
                difference = (t - times[i - 1]).total_seconds() * 1000000

                assert difference >= 1, (
                    "Expected unique timestamps (not within 1 microsecond), but time "
                    + '{} ("{}") is {}us from the previous one'.format(i, t, difference)
                )

                if difference == 1:
                    num_after_1us += 1

        assert num_after_1us > len(times) * 0.9, (
            "Expected at least 90% of the {} timestamps to be just ".format(len(times))
            + "1 microsecond after the previous timestamp, but only "
            + "{} of the timestamps satisfy that requirement -- ".format(num_after_1us)
            + "the test didn't run fast enough to ensure correct behavior"
        )


def _assert_time_within_tolerance(expected, actual):
    tolerance_seconds = 0.1
    difference = abs((actual - expected).total_seconds())
    assert (
        difference < tolerance_seconds
    ), 'Expected time to be "{}" +/- {} seconds but was "{}" for a {} second difference'.format(
        expected, tolerance_seconds, actual, difference
    )


def _gmt_now():
    return datetime.datetime.now(datetime.timezone.utc)
