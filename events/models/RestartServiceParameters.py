class RestartServiceParameters:

    def __init__(self,
                 service_name: str,
                 mode: str = 'replace'):
        self.service_name = service_name
        self.mode = mode

    def __hash__(self) -> int:
        return hash((self.service_name, self.mode))

    def __eq__(self, other) -> bool:
        if not isinstance(other, RestartServiceParameters):
            return NotImplemented
        return ((self.service_name, self.mode) ==
                (other.service_name, other.mode))
