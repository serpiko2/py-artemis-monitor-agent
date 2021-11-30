import sys
import traceback

from gi.repository import GLib


def schedule_function(fun: callable, *args, delay: int = 0, loop=False):
    print(f"scheduled: {fun}, schedule_function args", *(loop, )+args)
    GLib.timeout_add(delay, fun, *(loop, )+args)


def run_loop():
    loop = GLib.MainLoop()
    try:
        loop.run()
    except KeyboardInterrupt:
        kill_loop()


def kill_loop(error_code=0):
    loop = GLib.MainLoop()
    traceback.print_exc()
    loop.quit()
    sys.exit(error_code)
