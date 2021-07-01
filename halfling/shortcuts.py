import halfling


def add_build_task(builder, build_types_dict=None):

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
    halfling.tasks.add_task(
        "clean",
        lambda _: builder.clean()
    )


def add_build_and_clean_tasks(builder, build_types_dict=None):
    add_build_task(builder, build_types_dict)
    add_clean_task(builder)
