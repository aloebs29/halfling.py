from pathlib import Path, PurePath
import platform
import shutil

from halfling.compile import CompileOptions, force_compile, link, is_compile_needed


def build(config, build_type):
    print(f"Building {config.project_name}..")
    # create build + obj directory if they don't exist
    obj_dir = Path(config.build_dir, config.obj_dir)
    obj_dir.mkdir(parents=True, exist_ok=True)
    # create compile options
    options = CompileOptions(config, build_type)
    # we need to keep track of a flag indicating linking is required,
    # object file names in the case linking is required, and a file
    # modified times dictionary to save on f.stat() queries
    needs_link = False
    obj_fnames = []
    file_mtimes = {}
    # compile files as needed
    for src_fname in config.sources:
        src_fname = Path(src_fname)
        obj_fname = obj_dir / src_fname.with_suffix(".o").name

        if is_compile_needed(src_fname, obj_fname, file_mtimes):
            print(f"Compiling {src_fname}..")
            force_compile(config.compiler, src_fname, obj_fname, options)
            needs_link = True

        obj_fnames.append(obj_fname)

    if needs_link:
        # get windows-compatible exe name
        executable_name = PurePath(config.build_dir, config.project_name)
        if platform.system() == "Windows":
            executable_name = executable_name / ".exe"
        # link
        print(f"Linking {executable_name}..")
        link(config.compiler, obj_fnames, executable_name, options)
        print("Build successful.")
    else:
        print("Build up to date.")


def clean(config):
    shutil.rmtree(config.build_dir)
    print("Clean successful.")
