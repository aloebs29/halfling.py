from collections import namedtuple

_Task = namedtuple("_Task", ["run", "setup_args"])

tasks = {}


def add_task(name, run_func, setup_args_func=None):
    tasks[name] = _Task(run_func, setup_args_func)
