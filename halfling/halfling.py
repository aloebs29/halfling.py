import toml
from dataclasses import dataclass
import subprocess
from pathlib import Path, PurePath

FILEPATH = "halfling.toml"
OBJ_DIR = "obj"


@dataclass
class Config:
    project_name: str
    compiler: str
    sources: list
    build_dir: str = "build"


if __name__ == "__main__":
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
    subprocess.run([config.compiler] + obj_files +
                   ["-o", PurePath(config.build_dir, config.project_name)])
