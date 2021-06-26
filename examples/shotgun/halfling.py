from pathlib import Path
import shutil

import halfling

BUILD_DIR = Path(__file__).parent / "hbuild"

build_options = halfling.builders.cxx.BuildOptions(
    executable_name="shotgun.out",
    compiler="g++",
    build_dir=BUILD_DIR,
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


def build(args):
    if args.type == "debug":
        build_options.flags.extend(["-g"])
    else: # release
        build_options.flags.extend(["-O2"])

    halfling.builders.cxx.build(build_options, args.jobs)


def setup_build_args(parser):
    parser.add_argument("-t", "--type", type=str, choices=["debug", "release"],
                        default="release", help="controls build type; defaults to release")
    parser.add_argument("-j", "--jobs", type=int, default=None,
                        help="controls max processes to run build with; defaults to os.cpu_count()")


halfling.tasks.add_task("build", build, setup_build_args)

halfling.tasks.add_task(
    "clean",
    lambda _: shutil.rmtree(BUILD_DIR),
)
