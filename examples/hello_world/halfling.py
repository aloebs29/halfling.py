from pathlib import Path
import shutil

import halfling

BUILD_DIR = Path(__file__).parent / "build"

build_options = halfling.builders.cxx.BuildOptions(
    executable_name="hello_world.out",
    compiler="clang",
    build_dir=BUILD_DIR,
    sources=["main.c"],
)

halfling.tasks.add_task(
    "build",
    lambda _: halfling.builders.cxx.build(build_options),
)

halfling.tasks.add_task(
    "clean",
    lambda _: shutil.rmtree(BUILD_DIR),
)
