"""Shortcuts for common halfling tasks."""

import halfling


def add_build_task(builder, build_types_dict=None):
    """Adds a build task to halfling.

    Args:
        builder (halfling.builders.Builder): Builder to be used by the task.
        build_types_dict (dict of str, Callable[halfling.builders.BuildOptions]): Dictionary for 
            mapping build types to an associated function which alters the builder's options.

    Example:
        add_build_task(halfling.builders.CxxBuilder(my_options), {
                "debug": lambda options: options.flags.extend(['-g']),
                "release": lambda options: options.flags.extend(['-O2'])
            }
        )
    """
    def setup_build_args(parser):
        if build_types_dict is not None:
            default_build_type = next(iter(build_types_dict.keys()))
            parser.add_argument("-t", "--type", type=str, choices=build_types_dict.keys(),
                                default=default_build_type, 
                                help=f"controls build type; defaults to {default_build_type}")

        parser.add_argument("-j", "--jobs", type=int, default=None,
                            help="controls max processes to run build with; defaults to " + \
                                 "os.cpu_count()")

    def build(args):
        if build_types_dict is not None:
            # extend options based on type
            build_types_dict[args.type](builder.options)
        # build with # jobs passed in through CLI
        builder.build(args.jobs)


    halfling.tasks.add_task("build", build, setup_build_args)


def add_clean_task(builder):
    """Adds a clean task to halfling (removes build dir).

    Args:
        builder (halfling.builders.Builder): Builder associated with the clean operation (specifies
            build dir to be cleaned).
    """
    halfling.tasks.add_task(
        "clean",
        lambda _: builder.clean()
    )


def add_build_and_clean_tasks(builder, build_types_dict=None):
    """Adds a build task and clean task to halfling.

    Args:
        builder (halfling.builders.Builder): Builder to be used by the tasks.
        build_types_dict (dict of str, Callable[halfling.builders.BuildOptions]): Dictionary for 
            mapping build types to an associated function which alters the builder's options.

    Note:
        See add_build_task docstring for more information on the build_type_dict.
    """
    add_build_task(builder, build_types_dict)
    add_clean_task(builder)
