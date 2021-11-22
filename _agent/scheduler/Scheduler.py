import traceback
from gi.repository import GLib


class Job:

    def __init__(self, func, delay:int, *args):
        self.func = func
        self.delay = delay
        self.args = args

    def schedule(self):
        # hack for args always being an object when passed as argument
        schedule_function(self.func, self.delay, self.args) \
            if len(self.args) != 0 else schedule_function(self.func, self.delay)


def schedule_function(job, delay:int=0, *args):
    GLib.timeout_add(delay, job, *args)


def schedule_jobs(*jobs: Job):
    for job in jobs:
        job.schedule()


def run_loop():
    loop = GLib.MainLoop()
    try:
        loop.run()
    except KeyboardInterrupt:
        traceback.print_exc()
        loop.quit()
