import halfling

build_options = halfling.builders.CxxBuildOptions(
    executable_name="hello_world.out",
    build_dir="build",
    compiler="clang",
    sources=["main.c"],
)

halfling.shortcuts.add_build_and_clean_tasks(halfling.builders.CxxBuilder(build_options))
