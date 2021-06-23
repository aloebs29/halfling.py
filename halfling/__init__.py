"""Small, practical C/++ build system written in Python; supports gcc and clang."""

from pathlib import Path

# re-exports
from halfling.tasks.tasks import Task, add_task
from halfling.config import configure

# for internal usage
_HALFLING_ROOT_DIR = Path(__file__).parent
with open(_HALFLING_ROOT_DIR.parent / "VERSION") as f:
    _HALFLING_VERSION = f.read().strip()
