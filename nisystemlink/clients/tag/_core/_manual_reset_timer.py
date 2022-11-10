# -*- coding: utf-8 -*-

"""Implementation of ManualResetTimer."""

import datetime
import threading
import traceback
from types import TracebackType
from typing import Any, Callable, List, Optional, Type

import events
from nisystemlink.clients.core._internal._classproperty_support import (
    ClasspropertySupport,
)
from typing_extensions import final, Literal


@final
class ManualResetTimer(events.Events, metaclass=ClasspropertySupport):
    """Represents a timer for periodic background operations such that :meth:`start()`
    must be called to restart the timer each time the :attr:`elapsed` event is raised.

    Attributes:
        elapsed: An event that is triggered when the timer has elapsed.

    Example::

        def timer_elapsed():
            print("The timer elapsed!")

        my_timer.elapsed += timer_elapsed
    """

    def __init_subclass__(cls) -> None:
        raise TypeError("type 'ManualResetTimer' is not an acceptable base type")

    __events__ = ["elapsed"]
    # Under certain circumstances, mypy complains about the event not having a type hint
    # unless we specify it explicitly. (But we also need to delete the attribute so that
    # Events.__getattr__ can do its magic.)
    elapsed = None  # type: events._EventSlot
    del elapsed

    __null_timer_impl = None  # type: Optional[ManualResetTimer]

    @ClasspropertySupport.classproperty
    def null_timer(cls) -> "ManualResetTimer":
        """A timer that never fires."""
        if cls.__null_timer_impl is None:
            # Bypass the ManualResetTimer constructor, to make a timerless timer
            obj = cls.__new__(ManualResetTimer)
            super(ManualResetTimer, obj).__init__()  # but call the base constructor

            obj._thread = None
            obj._running = []  # used as mutable boolean; empty is False

            cls.__null_timer_impl = obj
        return cls.__null_timer_impl

    def __init__(self, interval: datetime.timedelta) -> None:
        """Initialize a timer that fires at the given interval a single time once
        :meth:`start()` has been called and then automatically stops.

        Args:
            interval: The amount of time after calling :meth:`start()` before
                :attr:`elapsed` is raised.

        Raises:
            ValueError: if ``interval`` is less than or equal to zero.
        """
        super().__init__()
        interval_secs = interval.total_seconds()
        if interval_secs <= 0:
            raise ValueError("interval cannot be <= 0")

        # Note: This _running flag means that the *thread* is running, not the timer
        self._running = [None]  # used as mutable boolean; non-empty is True
        self._timer_start = threading.Event()
        self._timer_cancel = threading.Event()
        self._thread = threading.Thread(
            target=self._run,
            args=[
                self._running,
                interval_secs,
                self._timer_start,
                self._timer_cancel,
                self.elapsed,
            ],
        )  # type: Optional[threading.Thread]
        self._thread.daemon = True
        self._thread.start()

    @property
    def can_start(self) -> bool:  # noqa: D401
        """Whether or not the timer is configured and can be started.

        A timer that isn't configured will never raise :attr:`elapsed`, even when
        :meth:`start()` is called.
        """
        return self._thread is not None

    def start(self) -> None:
        """Start the timer."""
        if self._running:
            self._timer_cancel.clear()
            self._timer_start.set()

    def stop(self) -> None:
        """Stop the timer."""
        if self._running:
            self._timer_cancel.set()

    @staticmethod
    def _run(
        running: List[None],
        interval: int,
        timer_start: threading.Event,
        timer_cancel: threading.Event,
        elapsed: Callable[[], None],
    ) -> None:
        while running:
            timer_start.wait()
            timer_start.clear()
            if running and not timer_cancel.wait(interval):
                try:
                    elapsed()
                except Exception:
                    traceback.print_exc()

    def __enter__(self) -> "ManualResetTimer":
        return self

    async def __aenter__(self) -> "ManualResetTimer":
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> Literal[False]:
        self.stop()
        for handler in list(self.elapsed):
            self.elapsed -= handler
        return False

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> Literal[False]:
        self.stop()
        for handler in list(self.elapsed):
            self.elapsed -= handler
        return False

    def __del__(self) -> None:
        self.stop()
        for handler in list(self.elapsed):
            self.elapsed -= handler

        # Stop the thread
        if self._running:
            self._running.clear()  # set our "mutable boolean" to False
            self._thread = None
            self._timer_cancel.set()
            self._timer_start.set()

    # Work around https://github.com/pyeve/events/issues/17
    def __getattr__(self, name: str) -> Any:
        if name in self.__events__:
            return super().__getattr__(name)
        else:
            return object.__getattribute__(self, name)

    # Fake method to tell mypy the type of our events
    def __type_hinting__(self) -> None:
        self.elapsed = type(self).elapsed  # type: events._EventSlot
