import sys
import traceback

from gi.repository import GLib

from _agent.scheduler.Job import Job


def schedule_function(fun: callable, args: tuple = None, delay: int = 0, loop=False):
    print(f"scheduled: {fun}, schedule_function args", *(loop, )+args)
    GLib.timeout_add(delay, fun, *(loop, )+args)


def schedule_job(job: Job):
    # hack for args always being an object when passed as argument
    schedule_function(job.func, job.args, delay=job.delay)


def schedule_jobs(*jobs: Job):
    for job in jobs:
        schedule_job(job)


def get_loop():
    return GLib.MainLoop()


def run_loop():
    loop = GLib.MainLoop()
    try:
        loop.run()
    except KeyboardInterrupt:
        traceback.print_exc()
        loop.quit()
        sys.exit(0)


def kill_loop():
    loop = GLib.MainLoop()
    traceback.print_exc()
    loop.quit()
    sys.exit(0)
