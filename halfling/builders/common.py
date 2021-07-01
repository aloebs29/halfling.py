from dataclasses import dataclass
import os
import shutil


@dataclass
class BuildOptions:
    build_dir: os.PathLike


class Builder:

    def __init__(self, options):
        self.options = options


    def build(self, num_processes=None):
        print("Unimplemented")


    def clean(self):
        shutil.rmtree(self.options.build_dir)

