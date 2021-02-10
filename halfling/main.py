import argparse
import toml
import sys

from config import Config
from exceptions import HalflingError
from tasks import build, clean

CONFIG_FILEPATH = "halfling.toml"


def run():
    # collect command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("task", type=str, choices=[
                        "build", "clean"], help="task to be run by halfling")
    args = parser.parse_args()

    try:
        # load config
        config = Config(**toml.load(CONFIG_FILEPATH))
        # run task
        if args.task == "build":
            build(config)
        elif args.task == "clean":
            clean(config)

    except FileNotFoundError as exc:
        print(f"{CONFIG_FILEPATH} file not found in current directory.")
        sys.exit(1)
    except toml.TomlDecodeError as exc:
        print(f"Invalid TOML syntax found in {CONFIG_FILEPATH}:\n{exc}")
        sys.exit(1)
    except HalflingError as exc:
        print("\n" + str(exc))
        sys.exit(1)


if __name__ == "__main__":
    run()
