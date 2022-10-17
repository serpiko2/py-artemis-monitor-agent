import sys

from gi.repository import GLib

import logging


class Scheduler:
    _main_loop = GLib.MainLoop()
    _logger = logging.getLogger(__name__)

    @classmethod
    def schedule_function(cls, fun: callable, poll: int = 10, *args):
        cls._logger.debug(f"scheduling function {fun.__name__}")
        GLib.timeout_add(int(poll), fun, *args)

    @classmethod
    def run_loop(cls):
        try:
            Scheduler._main_loop.run()
        except Exception as exc:
            cls.kill_loop(exc)

    @classmethod
    def kill_loop(cls, exc, error_code=0):
        cls._logger.error(exc)
        Scheduler._main_loop.quit()
        exit(error_code)
