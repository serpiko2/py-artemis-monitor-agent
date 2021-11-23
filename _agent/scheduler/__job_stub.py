from _agent.scheduler import Job


class __JobStub(Job):

    def __init__(self,
                 params,
                 delay: int = 0,
                 loop=False):
        super().__init__(delay, loop, params)
        self.success = None
        self.failed = None

    def callback(self, reply):
        print(f"{reply}")
        self.success = True
        pass

    def fallback(self, error):
        print(f"{error}")
        self.failed = True
        pass

    @staticmethod
    def execute(loop: bool, callback: callable, fallback: callable, params):
        """Find the service unit by it's name.
            :param:
                `name`:`the formatted service name as {name}.service`
                `loop`:`true or false to make it loop`
            :returns:
                `service_object_path`:`the service object path reference`
        """
        print(f"running an unimplemented job stub entrypoint: {loop, callback, fallback, params}")
        print(f"we should do something awesome here!")
        # return false to not loop
        return loop
