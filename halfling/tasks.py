from collections import namedtuple

_Task = namedtuple("_Task", ["run", "add_args"])

tasks = {}


def add_task(name, run_func, add_args_func=None):
    tasks[name] = _Task(run_func, add_args_func)
