"""Exposes functionality for adding tasks to halfling."""

from collections import namedtuple

_Task = namedtuple("_Task", ["run", "setup_args", "prerequisites"])
_tasks = {}


def add_task(name, run_func, setup_args_func=None, prerequisites=None):
    """Add a task to halfling.

    Args:
        name (str): Name to be used to run the task from the halfling CLI.
        run_func (Callable[argparse.Namespace]): Function to be called by task; receives parsed
            CLI args.
        setup_args_func (Callable[argparse.ArgumentParser]): Function to add arguments to the
            provided parser; optional.
        prerequisites (list of str): Name of tasks to be performed prior to running this task, in
            order. Arguments from prerequisite tasks will be added.
    """
    _tasks[name] = _Task(run_func, setup_args_func, prerequisites)
