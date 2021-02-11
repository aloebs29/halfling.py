import subprocess
from pathlib import Path, PurePath
import platform
import shutil

from halfling.exceptions import HalflingError, HalflingCompileError, HalflingLinkError

KEEP_OUTPUT_COLORS = "-fdiagnostics-color=always"


def build(config, build_type):
    print(f"Building {config.project_name}..")
    # create build + obj directory if they don't exist
    obj_dir = Path(config.build_dir, config.obj_dir)
    obj_dir.mkdir(parents=True, exist_ok=True)
    # create includes, defines
    includes = [f"-I{path}" for path in config.include_paths]
    defines = [f"-D{define}" for define in config.defines]
    # create flags
    flags = config.common_flags + [KEEP_OUTPUT_COLORS]
    if build_type == "debug":
        flags.extend(config.debug_flags)
    elif build_type == "release":
        flags.extend(config.release_flags)
    # compile object files
    obj_files = []
    for source in config.sources:
        # attempt compile
        print(f"Compiling {source}..")
        obj_file = obj_dir / PurePath(source).with_suffix(".o").name
        compile_proc = subprocess.run(
            [config.compiler, "-o", obj_file, "-c",
                source] + flags + includes + defines,
            capture_output=True)
        # if compile fails, raise with stderr info
        if compile_proc.returncode:
            raise HalflingCompileError(
                f"Error compiling {source}:\n{compile_proc.stderr.decode('ascii')}")
        # append obj file to list for linking
        obj_files.append(obj_file)

    # get windows-compatible exe name
    executable_name = PurePath(config.build_dir, config.project_name)
    if (platform.system() == "Windows"):
        executable_name = executable_name / ".exe"
    # build library paths, libraries
    lib_paths = [f"-L{path}" for path in config.library_paths]
    libs = [f"-l{lib}" for lib in config.libraries]
    # attempt link
    print(f"Linking {executable_name}..")
    link_proc = subprocess.run([config.compiler] +
                               obj_files + flags +
                               lib_paths + libs +
                               ["-o", executable_name],
                               capture_output=True)
    # if link fails, raise with stderr info
    if link_proc.returncode:
        raise HalflingLinkError(
            f"Error linking {executable_name}:\n{link_proc.stderr.decode('ascii')}")
    print(f"Build successful.")


def clean(config):
    shutil.rmtree(config.build_dir)
    print(f"Clean successful.")
