
class RestartListener:

    def __init__(self):
        self.load_state = None
        self.load_state_trigger = False
        self.active_state = None
        self.active_state_trigger = False
        self.status_code = None
        self.status_code_trigger = False

    def handle_load_state_monitor_event(self, *items, fun):
        print(f"handle monitor event {items}")
        self.load_state = items[0]
        self.load_state_trigger = True
        fun()


    def handle_active_state_monitor_event(self, *items, fun):
        print(f"handle monitor event {items}")
        self.active_state = items[0]
        self.active_state_trigger = True
        fun()


    def handle_exec_start_monitor_event(self, *items, fun):
        print(f"handle monitor event {items}")
        self.status_code = items[0][0][9]
        self.status_code_trigger = True
        fun()

