import toml
from dataclasses import dataclass
import subprocess
from pathlib import Path, PurePath
import platform

FILEPATH = "halfling.toml"
OBJ_DIR = "obj"


@dataclass
class Config:
    project_name: str
    compiler: str
    sources: list
    build_dir: str = "build"


def run():
    # load config
    config = Config(**toml.load(FILEPATH))
    # create build + obj directory if they don't exist
    obj_dir = Path(config.build_dir, OBJ_DIR)
    obj_dir.mkdir(parents=True, exist_ok=True)
    # compile object files
    obj_files = []
    for source in config.sources:
        obj_file = (obj_dir / source).with_suffix(".o")
        subprocess.run([config.compiler, "-o", obj_file, "-c", source])
        obj_files.append(obj_file)
    # link
    executable_name = PurePath(config.build_dir, config.project_name)
    if (platform.system() == "Windows"):
        executable_name = executable_name / ".exe"
    subprocess.run([config.compiler] + obj_files + ["-o", executable_name])


if __name__ == "__main__":
    run()
