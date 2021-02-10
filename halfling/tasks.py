import subprocess
from pathlib import Path, PurePath
import platform
import shutil

from exceptions import HalflingError, HalflingCompileError, HalflingLinkError

KEEP_OUTPUT_COLORS = "-fdiagnostics-color=always"


def build(config):
    print(f"Building {config.project_name}..")
    # create build + obj directory if they don't exist
    obj_dir = Path(config.build_dir, config.obj_dir)
    obj_dir.mkdir(parents=True, exist_ok=True)
    # compile object files
    obj_files = []
    for source in config.sources:
        # attempt compile
        print(f"Compiling {source}..")
        obj_file = (obj_dir / source).with_suffix(".o")
        compile_proc = subprocess.run(
            [config.compiler, "-o", obj_file, "-c",
                source, KEEP_OUTPUT_COLORS],
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
    # attempt link
    print(f"Linking {executable_name}..")
    link_proc = subprocess.run([config.compiler] + obj_files +
                               ["-o", executable_name, KEEP_OUTPUT_COLORS],
                               capture_output=True)
    # if link fails, raise with stderr info
    if link_proc.returncode:
        raise HalflingLinkError(
            f"Error linking {executable_name}:\n{link_proc.stderr.decode('ascii')}")
    print(f"Build successfull.")


def clean(config):
    shutil.rmtree(config.build_dir)
    print(f"Clean successful.")
