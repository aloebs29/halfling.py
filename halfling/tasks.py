from pathlib import Path, PurePath
import platform
import shutil

from compile import CompileOptions, run_compile, run_link


def run_build(config, build_type):
    print(f"Building {config.project_name}..")
    # create build + obj directory if they don't exist
    obj_dir = Path(config.build_dir, config.obj_dir)
    obj_dir.mkdir(parents=True, exist_ok=True)
    # create compile options
    options = CompileOptions(config, build_type)
    # compile object files
    obj_files = []
    for source in config.sources:
        print(f"Compiling {source}..")
        obj_file = obj_dir / PurePath(source).with_suffix(".o").name
        run_compile(config.compiler, source, obj_file, options)
        # append obj file to list for linking
        obj_files.append(obj_file)

    # get windows-compatible exe name
    executable_name = PurePath(config.build_dir, config.project_name)
    if platform.system() == "Windows":
        executable_name = executable_name / ".exe"
    # link
    print(f"Linking {executable_name}..")
    run_link(config.compiler, obj_files, executable_name, options)
    print("Build successful.")


def run_clean(config):
    shutil.rmtree(config.build_dir)
    print("Clean successful.")
