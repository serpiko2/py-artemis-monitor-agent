import traceback
from gi.repository import GLib


class Job:
    def __init__(self, func, delay:int):
        self.func = func
        self.delay = delay

    def schedule(self):
        schedule_function(self.func, self.delay)

def schedule_function(job, delay:int=0, *args):
    print(f"job: {job}, args: {args}")
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
