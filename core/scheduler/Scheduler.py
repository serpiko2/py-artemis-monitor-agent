import sys
import traceback

from gi.repository import GLib

from core.Logger import Logger


class Scheduler:
    _main_loop = GLib.MainLoop()
    _logger = Logger.get_logger("Scheduler")

    @staticmethod
    def schedule_function(fun: callable, poll: int = 10, *args):
        GLib.timeout_add(poll, fun, *args)

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
