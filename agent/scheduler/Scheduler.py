import traceback
from abc import ABC, abstractmethod

from gi.repository import GLib


class Job(ABC):

    def __init__(self, func, delay:int):
        self.func = func
        self.delay = delay

    @abstractmethod
    def schedule(self, *args):
        schedule_function(self.func, self.delay, args)

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
