from agent.ServiceStatusProcessor import ServiceStatusProcessor
import dbus.mainloop.glib
import traceback
from gi.repository import GLib
from agent.manager import DbusManager

class Job:
    def __init__(self, func, delay: int, loop: bool):
        self.func = func
        self.delay = delay
        self.loop = loop

def schedule_function(job, delay=0, loop=False):
    job._entrypoint(delay, loop)

def schedule_job(job: Job):
    job.func._entrypoint(job.delay, job.loop)

if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    schedule_job(
        Job(ServiceStatusProcessor(), 5, False)
    )
    loop = GLib.MainLoop()
    try:
        loop.run()
    except KeyboardInterrupt:
        traceback.print_exc()
        loop.quit()

