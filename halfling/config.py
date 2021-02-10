from dataclasses import dataclass


@dataclass
class Config:
    project_name: str
    compiler: str
    sources: list
    build_dir: str = "build"
    obj_dir: str = "obj"
