import sys
import traceback
from typing import overload

from gi.repository import GLib

from core.Logger import Logger


class Scheduler:
    _main_loop = GLib.MainLoop()
    _logger = Logger.get_logger("Scheduler")

    @staticmethod
    @overload
    def schedule_function(fun: callable, poll: int = 10):
        Scheduler._logger.info("No arg call for function")
        GLib.timeout_add(poll, fun)

    @staticmethod
    def schedule_function(fun: callable, *args, poll: int = 10):
        Scheduler._logger.info("Multi arg call for function")
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
