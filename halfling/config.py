from dataclasses import dataclass, field


@dataclass
class Config:
    # mandatory build info
    project_name: str
    compiler: str
    sources: list
    # output directories
    build_dir: str = "build"
    obj_dir: str = "obj"
    # compiler flags
    common_flags: list = field(default_factory=list)
    debug_flags: list = field(default_factory=lambda: ["-Og", "-g"])
    release_flags: list = field(default_factory=lambda: ["-O2"])
