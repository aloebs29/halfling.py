import argparse
import toml

from config import Config
from tasks import build, clean

FILEPATH = "halfling.toml"


def run():
    # collect command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("task", type=str, choices=[
                        "build", "clean"], help="task to be run by halfling")
    args = parser.parse_args()

    # load config
    config = Config(**toml.load(FILEPATH))

    # run task
    if args.task == "build":
        build(config)
    elif args.task == "clean":
        clean(config)


if __name__ == "__main__":
    run()
