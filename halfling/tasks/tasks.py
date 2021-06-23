tasks = {}

class Task:
    def run(self, args):
        print("Unimplemented!")

    def add_args(self, parser):
        pass


def add_task(name, task):
    tasks[name] = task
