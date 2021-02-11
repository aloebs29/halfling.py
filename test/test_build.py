import unittest
import subprocess
import pathlib
import sys

SCRIPT_PATH = pathlib.Path(__file__).parent.absolute()
PROJECT_ROOT_PATH = SCRIPT_PATH.parent
HALFLING_ROOT_PATH = PROJECT_ROOT_PATH / "halfling"
HALFLING_MAIN_PATH = HALFLING_ROOT_PATH / "main.py"
EXAMPLES_DIR_PATH = PROJECT_ROOT_PATH / "examples"
TEST_DATA_DIR_PATH = SCRIPT_PATH / "data"

# NOTE: These are high-level functional tests that actually build projects,
# they may take a few seconds to run.
# These can be run from root with "python3 -m unittest discover -s test"


class TestBuildSuccess(unittest.TestCase):
    def test_hello_world(self):
        # build runs..
        build_proc = subprocess.run(
            ["python3", HALFLING_MAIN_PATH, "build"],
            cwd=(EXAMPLES_DIR_PATH / "hello_world"),
            capture_output=True)
        self.assertEqual(0, build_proc.returncode)
        # output is correct..
        executable = list((EXAMPLES_DIR_PATH / "hello_world" /
                           "build").glob("hello_world*"))[0]
        hello_proc = subprocess.run(
            [executable],
            capture_output=True)
        self.assertEqual(0, hello_proc.returncode)
        self.assertEqual(b"Hello world!\n", hello_proc.stdout)

    def test_shotgun(self):
        # build runs..
        build_proc = subprocess.run(
            ["python3", HALFLING_MAIN_PATH, "build"],
            cwd=(EXAMPLES_DIR_PATH / "shotgun"),
            capture_output=True)
        self.assertEqual(0, build_proc.returncode)
        # executable runs
        executable = list((EXAMPLES_DIR_PATH / "shotgun" /
                           "build_output").glob("shotgun*"))[0]
        shotgun_proc = subprocess.run(
            [executable],
            capture_output=True)
        self.assertEqual(0, shotgun_proc.returncode)
        self.assertTrue(
            b"Calculating 2 + 3 with function in another file.." in shotgun_proc.stdout)


class TestBuildFailure(unittest.TestCase):
    def test_compile_error(self):
        build_proc = subprocess.run(
            ["python3", HALFLING_MAIN_PATH, "build"],
            cwd=(TEST_DATA_DIR_PATH / "compile_error"),
            capture_output=True)
        self.assertEqual(1, build_proc.returncode)
        self.assertTrue(b"Error compiling" in build_proc.stdout)

    def test_link_error(self):
        build_proc = subprocess.run(
            ["python3", HALFLING_MAIN_PATH, "build"],
            cwd=(TEST_DATA_DIR_PATH / "link_error"),
            capture_output=True)
        self.assertEqual(1, build_proc.returncode)
        self.assertTrue(b"Error linking" in build_proc.stdout)

    def test_toml_invalid(self):
        build_proc = subprocess.run(
            ["python3", HALFLING_MAIN_PATH, "build"],
            cwd=(TEST_DATA_DIR_PATH / "toml_invalid"),
            capture_output=True)
        self.assertEqual(1, build_proc.returncode)
        self.assertTrue(b"Invalid TOML" in build_proc.stdout)

    def test_toml_missing(self):
        build_proc = subprocess.run(
            ["python3", HALFLING_MAIN_PATH, "build"],
            cwd=(TEST_DATA_DIR_PATH / "toml_missing"),
            capture_output=True)
        self.assertEqual(1, build_proc.returncode)
        self.assertTrue(b"file not found" in build_proc.stdout)
