class RestartServiceParameters:

    def __init__(self,
                 service_name: str,
                 mode: str = 'replace'):
        self.service_name = service_name
        self.mode = mode
