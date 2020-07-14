import datetime
import time

from systemlink.clients.tag._core._manual_reset_timer import ManualResetTimer


class TestManualResetTimer:
    def test__event_raises__timer_continues(self):
        data = []
        interval = datetime.timedelta(milliseconds=100)
        with ManualResetTimer(interval) as uut:

            def callback():
                try:
                    data.append(None)
                    raise RuntimeError()
                finally:
                    uut.start()

            uut.elapsed += callback

            uut.start()
            time.sleep(0.280)

            assert 2 <= len(data) <= 3
