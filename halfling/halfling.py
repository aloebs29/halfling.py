import toml
from dataclasses import dataclass

FILEPATH = "./halfling.toml"


@dataclass
class Config:
    project_name: str
    compiler: str
    sources: list


if __name__ == "__main__":
    config = Config(**toml.load(FILEPATH))
    print(config)
