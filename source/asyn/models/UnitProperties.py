from source.config.MonitorConfig import MonitorConfig


class UnitProperties:

    def __init__(self):
        self.exec_start = []
        self.load_state = False
        self.active_state = False
        self.service_name = MonitorConfig.service_name

    def set_exec_start(self, exec_start):
        self.exec_start = exec_start

    def set_load_state(self, load_state):
        self.load_state = load_state

    def set_active_state(self, active_state):
        self.active_state = active_state

    def all_read(self):
        return self.exec_start and self.load_state and self.active_state
