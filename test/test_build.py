import unittest
import subprocess
import pathlib

SCRIPT_PATH = pathlib.Path(__file__).parent.absolute()
HALFLING_MAIN_PATH = SCRIPT_PATH / "../halfling/main.py"
DATA_DIR_PATH = SCRIPT_PATH / "data"


class TestBuild(unittest.TestCase):
    def test_hello_world(self):
        # build runs..
        build_proc = subprocess.run(
            ["python3", HALFLING_MAIN_PATH, "build"],
            cwd=(DATA_DIR_PATH / "hello_world"),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)
        self.assertEqual(0, build_proc.returncode)
        # output is correct..
        executable = list((DATA_DIR_PATH / "hello_world" /
                           "build").glob("hello_world*"))[0]
        hello_proc = subprocess.run(
            [executable],
            capture_output=True)
        self.assertEqual(0, hello_proc.returncode)
        self.assertEqual(b"Hello world!\n", hello_proc.stdout)

    def test_compile_error(self):
        build_proc = subprocess.run(
            ["python3", HALFLING_MAIN_PATH, "build"],
            cwd=(DATA_DIR_PATH / "compile_error"),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)
        self.assertEqual(1, build_proc.returncode)

    def test_link_error(self):
        build_proc = subprocess.run(
            ["python3", HALFLING_MAIN_PATH, "build"],
            cwd=(DATA_DIR_PATH / "link_error"),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)
        self.assertEqual(1, build_proc.returncode)

    def test_toml_invalid(self):
        build_proc = subprocess.run(
            ["python3", HALFLING_MAIN_PATH, "build"],
            cwd=(DATA_DIR_PATH / "toml_invalid"),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)
        self.assertEqual(1, build_proc.returncode)

    def test_toml_missing(self):
        build_proc = subprocess.run(
            ["python3", HALFLING_MAIN_PATH, "build"],
            cwd=(DATA_DIR_PATH / "toml_missing"),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)
        self.assertEqual(1, build_proc.returncode)