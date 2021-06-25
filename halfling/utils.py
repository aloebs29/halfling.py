from multiprocessing.dummy import Pool, Lock
from pathlib import Path

# for internal usage
_HALFLING_ROOT_DIR = Path(__file__).parent
with open(_HALFLING_ROOT_DIR.parent / "VERSION") as f:
    _HALFLING_VERSION = f.read().strip()


class JobPool:
    def __init__(self, num_processes):
        self.pool = Pool(num_processes)
        self.pending = 0
        self.exc = None
        self.mutex = Lock()

    def _job_callback(self, _):
        self.mutex.acquire()
        self.pending -= 1
        self.mutex.release()

    def _job_err_callback(self, exc):
        self.mutex.acquire()
        self.exc = exc
        self.mutex.release()

    def submit_job(self, func, args):
        self.pending += 1
        self.pool.apply_async(
            func, args, callback=self._job_callback, error_callback=self._job_err_callback)

    def wait_for_done(self):
        while True:
            # copy locked values
            self.mutex.acquire()
            pending = self.pending
            exc = self.exc
            self.mutex.release()
            # check for exception
            if exc:
                self.pool.terminate()
                self.pool.join()
                raise self.exc
            # check for done
            if pending == 0:
                return
