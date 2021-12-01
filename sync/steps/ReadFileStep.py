import io

from core.scheduler import Scheduler


class FileHandler:

    def __init__(self, callback):
        self._force_exit = False
        self._is_active = False
        self.callback = callback

    def force_exit(self):
        if self._is_active:
            self._force_exit = True
            print(f"forcing exit {self._force_exit}, with active state {self._is_active}")

    def seek_to_end_and_tail(self, filename):
        print(f"scheduling new handler for {filename}")
        self._is_active = True
        file = FileHandler.find_and_open(filename)
        file.seek(0, io.SEEK_END)
        Scheduler.schedule_function(self._schedule_in_loop,
                                    file,
                                    delay=10,
                                    loop=True)

    def _schedule_in_loop(self, loop, file):
        print(f"scheduled function run, status: _force_exit={self._force_exit}, "
              f"_is_active={self._is_active}")
        if not self._force_exit:
            self._is_active = self.read_line_from_file(loop, file)
            return self._is_active
        else:
            print(f"Exit Forced {self._force_exit}, with active state {self._is_active}")
            self._force_exit = False
            self._is_active = False
            return False

    def read_line_from_file(self, loop, file):
        line = file.readline()
        print(f"reading line {line}")
        result = FileHandler.check_codes(line)
        if result == "Failed":
            loop = False
            print(f"ending loop on failure, restarting")
            self.callback()
        elif result == "Success":
            loop = False
            print(f"ending loop on success, doing nothing")
        return loop
