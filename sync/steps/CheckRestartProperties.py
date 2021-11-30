class CheckRestartProperties:
    load_state: str
    active_state: str
    exec_start: str

    def __init__(self, load_state, active_state, exec_start):
        self.load_state = load_state
        self.active_state = active_state
        self.exec_start = exec_start
