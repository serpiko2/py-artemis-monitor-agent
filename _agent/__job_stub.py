from _agent.manager import Sysd
from _agent.scheduler.Scheduler import Job


def entrypoint(loop: bool, callback: callable, fallback: callable, *items):
    """Find the service unit by it's name.
        :param:
            `name`:`the formatted service name as {name}.service`
            `loop`:`true or false to make it loop`
        :returns:
            `service_object_path`:`the service object path reference`
    """
    Sysd.get_manager().GetUnit(
        *items,
        reply_handler=callback,
        error_handler=fallback
    )
    # return false to not loop
    return loop


class __JobStub(Job):

    def __init__(self,
                 params,
                 delay: int = 0,
                 loop=False):
        super().__init__(entrypoint, delay, loop, params)
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
