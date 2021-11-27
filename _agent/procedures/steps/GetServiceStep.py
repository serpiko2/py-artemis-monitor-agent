import dbus

from _agent.manager import Sysd
from _agent.procedures.steps.Step import Step


class GetServiceStep(Step):

    def __init__(self, service_name: str):
        self.service_name = service_name

    def apply(self) -> str:
        return Sysd.get_sysd_manager().GetUnit(
            self.service_name
        )
