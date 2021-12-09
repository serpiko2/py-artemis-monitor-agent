import sys
import traceback

from gi.repository import GLib


class Scheduler:
    _main_loop = GLib.MainLoop()

    @staticmethod
    def schedule_function(fun: callable, *args, poll: int = 10):
        GLib.timeout_add(poll, fun, args)

    @staticmethod
    def run_loop():
        try:
            Scheduler._main_loop.run()
        except KeyboardInterrupt:
            Scheduler.kill_loop()

    @staticmethod
    def kill_loop(error_code=0):
        traceback.print_exc()
        Scheduler._main_loop.quit()
        sys.exit(error_code)
