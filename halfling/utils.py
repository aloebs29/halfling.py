"""Common utility functions used internally by halfling which may be useful to users."""

from multiprocessing.dummy import Pool, Lock
from pathlib import Path

# for internal usage
_HALFLING_ROOT_DIR = Path(__file__).parent
with open(_HALFLING_ROOT_DIR.parent / "VERSION") as f:
    _HALFLING_VERSION = f.read().strip()


class JobPool:
    """Multiprocessing job pool which captures and re-raises exceptions in jobs.

    Args:
        num_processes (int): Max number of processes to be used by job pool. Use 'None' for 
            os.cpu_count().

    Note:
        Exceptions will be re-raised in the process which wait_for_done is called.
    """

    def __init__(self, num_processes):
        self._pool = Pool(num_processes)
        self._pending = 0
        self._exc = None
        self._mutex = Lock()

    def _job_callback(self, _):
        self._mutex.acquire()
        self._pending -= 1
        self._mutex.release()

    def _job_err_callback(self, exc):
        self._mutex.acquire()
        self._exc = exc
        self._mutex.release()

    def submit_job(self, func, args):
        """Submit a job to the pool."""
        self._pending += 1
        self._pool.apply_async(
            func, args, callback=self._job_callback, error_callback=self._job_err_callback)

    def wait_for_done(self):
        """Wait for all jobs to complete."""
        while True:
            # copy locked values
            self._mutex.acquire()
            pending = self._pending
            exc = self._exc
            self._mutex.release()
            # check for exception
            if exc:
                self._pool.terminate()
                self._pool.join()
                raise self._exc
            # check for done
            if pending == 0:
                return
