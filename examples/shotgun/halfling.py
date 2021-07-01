from pathlib import Path

import halfling

build_options = halfling.builders.CxxBuildOptions(
    executable_name="shotgun.out",
    compiler="g++",
    build_dir=Path(__file__).parent / "hbuild",
    sources=[
        "src/main.cpp",
        "src/add.cpp",
        "src/sub.cpp",
    ],
    obj_dir="hobj",
    flags=["-Wall"],
    include_paths=["lib/mul/inc"],
    defines=["DEFINED_IN_PY", "ALSO_DEFINED_IN_PY"],
    lib_paths=["lib/mul"],
    libs=["mul"]
)

halfling.shortcuts.add_build_and_clean_tasks(
    halfling.builders.CxxBuilder(build_options),
    {
        "debug": lambda options: options.flags.extend(["-g"]),
        "release": lambda options: options.flags.extend(["-O2"])
    }
)
