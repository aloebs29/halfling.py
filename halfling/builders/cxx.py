"""Exposes functionality for compiling and linking c programs."""

from dataclasses import dataclass, field
import os
import subprocess
from pathlib import Path

from halfling.builders import common
from halfling.exceptions import HalflingCompileError, HalflingLinkError
from halfling.utils import JobPool

KEEP_OUTPUT_COLORS = "-fdiagnostics-color=always"
WRITE_DEPENDENCY_INFO = "-MMD"


@dataclass
class CxxBuildOptions(common.BuildOptions):
    # mandatory
    executable_name: os.PathLike
    compiler: str
    sources: list

    # optional
    obj_dir: os.PathLike = "obj"

    flags: list = field(default_factory=list)
    include_paths: list = field(default_factory=list)
    defines: list = field(default_factory=list)
    lib_paths: list = field(default_factory=list)
    libs: list = field(default_factory=list)

    
    def combine_flags(self):
        return [f"-I{path}" for path in self.include_paths] + \
            [f"-D{define}" for define in self.defines] + \
            [f"-L{path}" for path in self.lib_paths] + \
            [f"-l{lib}" for lib in self.libs] + \
            self.flags + [KEEP_OUTPUT_COLORS, WRITE_DEPENDENCY_INFO]


class CxxBuilder(common.Builder):

    def build(self, num_processes=None):
        """Builds project.

        Args:
            num_processes (int): Number of processes to run the build with. If 'None'
                is provided for this argument, will default to os.cpu_count().

        Returns:
            None

        Raises:
            HalfingError: if any build compilation errors occur. Will contain 
            compiler error message.
        """
        print(f"Building {self.options.executable_name}..")
        # create build + obj directory if they don't exist
        build_dir = Path(self.options.build_dir)
        obj_dir = build_dir / self.options.obj_dir
        obj_dir.mkdir(parents=True, exist_ok=True)

        # we need to keep track of a flag indicating linking is required,
        # object file names in the case linking is required, and a file
        # modified times dictionary to save on f.stat() queries
        needs_link = False
        obj_fnames = []
        file_mtimes = {}

        # compile files as needed in a thread pool
        pool = JobPool(num_processes)
        for src_fname in self.options.sources:
            src_fname = Path(src_fname)
            obj_fname = obj_dir / src_fname.with_suffix(".o").name

            if is_compile_needed(src_fname, obj_fname, file_mtimes):
                pool.submit_job(compile_file, (self.options.compiler, src_fname, obj_fname,
                                               self.options.combine_flags()))
                needs_link = True

            obj_fnames.append(obj_fname)

        pool.wait_for_done()

        # link
        executable_path = self.options.build_dir / self.options.executable_name
        if needs_link or not executable_path.exists():
            link(self.options.compiler, obj_fnames, executable_path, self.options.combine_flags())
            print("Build successful.")
        else:
            print("Build up to date.")


def _are_deps_out_of_date(deps_fname, obj_mtime, file_mtimes):
    # deps file should always exist, if they don't, just call it OOD
    if not deps_fname.exists():
        return True
    # read deps file
    with open(deps_fname, "r") as dep_file:
        deps = dep_file.read().split(":")[1].replace("\\", "").split()
        # loop through dependencies, returning true if we find one OOD
        for dep in deps:
            # Add file to mtimes dict
            if dep not in file_mtimes:
                file_mtimes[dep] = Path(dep).stat().st_mtime

            if obj_mtime < file_mtimes[dep]:
                return True

    # if execution reaches here, all dependencies are up to date
    return False


def is_compile_needed(src_fname, obj_fname, file_mtimes):
    """Checks if object file is out of date and need recompile.

    Args:
        src_fname (str): Filename of the source associated with the object file.
        obj_fname (str): Object filename.
        file_mtimes (dict): {filename, modified_time} Dictionary of file 
            modified times evaluated thus far. Will be appended to by this
            function if new files are evaluated.

    Returns:
        bool: True if object file is out of date
    """
    # add source file to mtimes dict
    if str(src_fname) not in file_mtimes:
        file_mtimes[str(src_fname)] = src_fname.stat().st_mtime
    # if obj doesn't exist, we need compile
    if not obj_fname.exists():
        return True
    # if obj is out of date, we need compile
    obj_mtime = obj_fname.stat().st_mtime
    if obj_mtime < file_mtimes[str(src_fname)]:
        return True
    # If source is up to date, check dependencies
    return _are_deps_out_of_date(obj_fname.with_suffix(".d"), obj_mtime, file_mtimes)


def compile_file(compiler, src_fname, obj_fname, flags=[]):
    """Runs compilation in subprocess regardless of whether obj is out of date.

    Args:
        compiler (str): Compiler command to be used.
        src_fname (str): Filename of source to be compiled.
        obj_fname (str): Filename of object file to be output.
        flags (list): List of flags to be passed to the compiler.

    Returns:
        None

    Raises:
        HalflingCompileError: if process fails, contains compiler error msg.
    """
    print(f"Compiling {src_fname}..")
    proc = subprocess.run([compiler, "-o", obj_fname, "-c", src_fname] + flags,
                          capture_output=True)
    if proc.returncode:
        raise HalflingCompileError(
            f"Error compiling {src_fname}:\n{proc.stderr.decode('utf-8')}")
    # catch warning output
    if proc.stderr:
        print(proc.stderr.decode("utf-8"))


def link(compiler, infiles, outfile, flags=[]):
    """Runs link in subprocess.

    Args:
        compiler (str): Compiler command to be used.
        infiles (list): List of obj files to be linked
        outfile (str): Filename of executable to be output.
        flags (list): List of flags to be passed to the compiler.

    Returns:
        None

    Raises:
        HalflingCompileError: if process fails, contains compiler error msg.
    """
    print(f"Linking {outfile}..")
    proc = subprocess.run([compiler] + infiles + flags + ["-o", outfile],
                          capture_output=True)
    # if link fails, raise with stderr info
    if proc.returncode:
        raise HalflingLinkError(
            f"Error linking {outfile}:\n{proc.stderr.decode('utf-8')}")
    # catch warning output
    if proc.stderr:
        print(proc.stderr.decode("utf-8"))
