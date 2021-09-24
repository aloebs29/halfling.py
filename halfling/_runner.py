"""Task runner called by halfling CLI command."""

import argparse
import sys
import importlib.util

from halfling.exceptions import HalflingError
from halfling.tasks import _tasks
from halfling.utils import _HALFLING_VERSION, get_project_base_dir

# TODO (aloebs29): search up directories for this file if it is not found in the current dir. This
# would allow the halfling CLI command to be called anywhere within a project.
_EXTENSION_MODULE_NAME = "extension"
_EXTENSION_FILENAME = "halfling.py"


def _load_extension(extension_path):
    extension_spec = importlib.util.spec_from_file_location(_EXTENSION_MODULE_NAME, 
                                                            extension_path)
    extension_module = importlib.util.module_from_spec(extension_spec)
    sys.modules[_EXTENSION_MODULE_NAME] = extension_module
    return extension_spec.loader.exec_module(extension_module)


def _setup_task_args(subparser, task):
    if task.prerequisites is not None:
        for prerequisite in task.prerequisites:
            _setup_task_args(subparser, _tasks[prerequisite])

    if task.setup_args is not None:
        task.setup_args(subparser)


def _run_task(args, task):
    if task.prerequisites is not None:
        for prerequisite in task.prerequisites:
            _run_task(args, _tasks[prerequisite])

    task.run(args)


def _collect_command_line_args():
    parser = argparse.ArgumentParser(description="halfling build and automation tool.")
    parser.add_argument("--version", action="store_true", help="display the version string")
    
    subparsers = parser.add_subparsers()
    for name, task in _tasks.items():
        task_parser = subparsers.add_parser(name)
        _setup_task_args(task_parser, task)
        task_parser.set_defaults(task=task) # store the task itself on the Namespace

    return parser.parse_args()


def run():
    # attempt to load extension
    try:
        extension_module = _load_extension(get_project_base_dir() / _EXTENSION_FILENAME)
    except FileNotFoundError:
        # only warn if no extension, that way --version, --help, etc can be run from any directory
        print(f"Warning: {_EXTENSION_FILENAME} file not found in current directory.")
    except SyntaxError as exc:
        print(f"Invalid syntax found in {_EXTENSION_FILENAME}.")
        # raise so the user gets the familiar python stack trace
        raise

    # collect args & run
    try:
        args = _collect_command_line_args()
        if args.version:
            print(f"{_HALFLING_VERSION}")
        elif hasattr(args, "task"):
            _run_task(args, args.task)
        else:
            print("No arguments provided. Type 'halfling -h' for help.")
    except HalflingError as exc:
        print("\n" + str(exc))
        sys.exit(1)
