"""Common functionality for builders."""

from dataclasses import dataclass
import os
import shutil


@dataclass
class BuildOptions:
    """Data structure containing build options."""

    build_dir: os.PathLike


class Builder:
    """Interface for builders; intended to be subclassed by language-specific builders.

    Args:
        options (BuildOptions): Build options.
    """

    def __init__(self, options):
        self.options = options


    def build(self, num_processes=None):
        """Build according to the options specified in the constructor.

        Args:
            num_processes (int): Number of processes to be used by the build; defaults to
                os.cpu_count().
        """
        print("Unimplemented")


    def clean(self):
        """Remove the build directory."""
        shutil.rmtree(self.options.build_dir)

