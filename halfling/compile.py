import subprocess

from exceptions import HalflingCompileError, HalflingLinkError

KEEP_OUTPUT_COLORS = "-fdiagnostics-color=always"
WRITE_DEPENDENCY_INFO = "-MMD"


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


def run_compile(compiler, infile, outfile, options):
    proc = subprocess.run([compiler, "-o", outfile, "-c", infile] +
                          options.flags + options.includes + options.defines,
                          capture_output=True)
    if proc.returncode:
        raise HalflingCompileError(
            f"Error compiling {infile}:\n{proc.stderr.decode('ascii')}")


def run_link(compiler, infiles, outfile, options):
    link_proc = subprocess.run([compiler] + infiles + options.flags +
                               options.lib_paths +
                               options.libs + ["-o", outfile],
                               capture_output=True)
    # if link fails, raise with stderr info
    if link_proc.returncode:
        raise HalflingLinkError(
            f"Error linking {outfile}:\n{link_proc.stderr.decode('ascii')}")
