from pathlib import Path

import halfling

build_options = halfling.builders.CxxBuildOptions(
    executable_name="link_error.out",
    compiler="clang++",
    build_dir=Path(__file__).parent / "build",
    sources=["main.cpp"],
)

halfling.shortcuts.add_build_and_clean_tasks(halfling.builders.CxxBuilder(build_options))
