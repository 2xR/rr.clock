import contextlib
import time

__version__ = "0.1.0"
__author__ = "Rui Rei"
__copyright__ = "Copyright 2017 {author}".format(author=__author__)
__license__ = "MIT"


class Timer:
    """A timer combines two time trackers in a single object (for cpu and wall time), providing a
    `.tracking()` context manager that activates both trackers. The elapsed time of the
    individual trackers can be consulted through the `.cpu` and `.wall` properties.

    Example usage:

        import time
        from rr.timer import Timer

        def busy_sleep(duration):
            start = time.time()
            while time.time() - start < duration:
                pass

        timer = Timer()
        print(timer)
        with timer.tracking():
            assert timer.active
            print(timer)
            time.sleep(1)
            print(timer)
            busy_sleep(1)
        assert not timer.active
        print(timer)
    """

    def __init__(self):
        self._cpu = TimeTracker(time_func=time.process_time)
        self._wall = TimeTracker(time_func=time.time)

    def __repr__(self):
        return "<{} @{:x}>".format(str(self), id(self))

    def __str__(self):
        return "{}(cpu={}, wall={}, active={})".format(
            type(self).__name__, self.cpu, self.wall, self.active)

    @property
    def cpu(self):
        """Obtain the cpu time elapsed so far."""
        return self._cpu.elapsed

    @property
    def wall(self):
        """Obtain the wall clock time elapsed so far."""
        return self._wall.elapsed

    @property
    def active(self):
        return self._cpu.active or self._wall.active

    def clear(self):
        self._cpu.clear()
        self._wall.clear()

    reset = clear

    def start(self):
        self._cpu.start()
        self._wall.start()

    def stop(self):
        self._cpu.stop()
        self._wall.stop()

    @contextlib.contextmanager
    def tracking(self):
        with self._cpu.tracking(), self._wall.tracking():
            yield


class TimeTracker:
    """Tracker object for tracking time using a given time function."""

    def __init__(self, time_func):
        self._time_func = time_func
        self._elapsed = 0.0
        self._track_count = 0
        self._track_start = None

    def __repr__(self):
        return "<{} @{:x}>".format(str(self), id(self))

    def __str__(self):
        return "{}({}: {} [{}])".format(
            type(self).__name__,
            self._time_func.__name__,
            self._elapsed,
            self._track_count,
        )

    @property
    def active(self):
        return self._track_count > 0

    @property
    def elapsed(self):
        if self._track_count > 0:
            return self._elapsed + (self._time_func() - self._track_start)
        else:
            return self._elapsed

    def clear(self):
        if self._track_count > 0:
            raise RuntimeError("cannot reset time tracker (currently active)")
        self._elapsed = 0.0

    reset = clear

    def start(self):
        if self._track_count == 0:
            self._track_start = self._time_func()
        self._track_count += 1

    def stop(self):
        if self._track_count > 0:
            self._track_count -= 1
            if self._track_count == 0:
                self._elapsed += self._time_func() - self._track_start
                self._track_start = None

    @contextlib.contextmanager
    def tracking(self):
        self.start()
        try:
            yield self
        finally:
            self.stop()
