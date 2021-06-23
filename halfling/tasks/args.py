class OptionalArg:

    def __init__(self, flags, value_type, choices, help_text):
        self.flags = flags
        self.value_type = value_type
        self.choices = choices
        self.help_text = help_text


    def add_to_parser(parser):
        if isinstance(self.flags, list):
            parser.add_argument(*self.flags, type=self.value_type, choices=self.choices,
                                help=self.help_text)
        else:
            parser.add_argument(self.flags, type=self.value_type, choices=self.choices,
                                help=self.help_text)

def make_build_type_arg(choices=["debug", "release"], default="release"):
    return OptionalArg(["-t", "--type"], str, choices, default, 
                       f"controls build type; defaults to {default}.")

def make_jobs_arg(default=None):
    return OptionalArg(["-j", "--jobs"], int, default,
                       "controls max processes to run build with; defaults to os.cpu_count()")

# collect command line arguments
# parser = argparse.ArgumentParser()
# parser.add_argument("task", type=str, choices=[
#                     "build", "clean"], help="task to be run by halfling")
# parser.add_argument("-t", "--type", type=str, choices=["debug", "release"],
#                     default="release", help="controls build type; defaults to release")
# parser.add_argument("-j", "--jobs", type=int, default=None,
#                     help="controls max processes to run build with; defaults to os.cpu_count()")
# args = parser.parse_args()
