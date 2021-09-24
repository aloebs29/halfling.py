import halfling

# Common build options used by all types
build_options = halfling.builders.CxxBuildOptions(
    executable_name="shotgun.out",
    compiler="g++",
    build_dir="hbuild",
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
    libs=["mul"],
    create_compile_flags_txt=True,
)

# Add build and clean tasks to halfling
halfling.shortcuts.add_build_and_clean_tasks(
    halfling.builders.CxxBuilder(build_options),
    # The build_types_dict allows users to specify custom build types which can be selected with
    # the -t/--type CLI option. The default will be the first build type specified in the dict
    # (if you're using python 3.7+, and most likely if you're using python 3.6).
    #
    # Each build type must provide a function which takes one argument (the build options data
    # structure).
    #
    # The build_types_dict defaults to None, in which case, there will be no -t/--type CLI option.
    build_types_dict={
        "debug": lambda options: options.flags.extend(["-g"]),
        "release": lambda options: options.flags.extend(["-O2"])
    }
)


# Add a custom task
def my_task(args):
    print(f"echo: {args.echo}")


def setup_my_task_args(parser):
    parser.add_argument("echo", type=str, help="string to echo back")


halfling.tasks.add_task("my_task", my_task, setup_my_task_args)

# Execute arbitrary code at load time. This probably isn't useful, its more for the sake of
# demonstrating that this is just normal python code.
print("Extension file loaded.")
