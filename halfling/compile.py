import subprocess
from pathlib import Path

from halfling.exceptions import HalflingCompileError, HalflingLinkError

KEEP_OUTPUT_COLORS = "-fdiagnostics-color=always"
WRITE_DEPENDENCY_INFO = "-MMD"


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


class CompileOptions:
    """Contains options for compiling and linking"""

    def __init__(self, config, build_type):
        self.includes = [f"-I{path}" for path in config.include_paths]
        self.defines = [f"-D{define}" for define in config.defines]
        self.lib_paths = [f"-L{path}" for path in config.library_paths]
        self.libs = [f"-l{lib}" for lib in config.libraries]

        self.flags = config.common_flags + \
            [KEEP_OUTPUT_COLORS, WRITE_DEPENDENCY_INFO]
        if build_type == "debug":
            self.flags.extend(config.debug_flags)
        elif build_type == "release":
            self.flags.extend(config.release_flags)


def force_compile(compiler, src_fname, obj_fname, options):
    print(f"Compiling {src_fname}..")
    proc = subprocess.run([compiler, "-o", obj_fname, "-c", src_fname] +
                          options.flags + options.includes + options.defines,
                          capture_output=True)
    if proc.returncode:
        raise HalflingCompileError(
            f"Error compiling {src_fname}:\n{proc.stderr.decode('ascii')}")


def link(compiler, infiles, outfile, options):
    print(f"Linking {outfile}..")
    link_proc = subprocess.run([compiler] + infiles + options.flags +
                               options.lib_paths +
                               options.libs + ["-o", outfile],
                               capture_output=True)
    # if link fails, raise with stderr info
    if link_proc.returncode:
        raise HalflingLinkError(
            f"Error linking {outfile}:\n{link_proc.stderr.decode('ascii')}")


def is_compile_needed(src_fname, obj_fname, file_mtimes):
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
