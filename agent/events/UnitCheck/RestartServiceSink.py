from agent.events.Events import Subscriber
from agent.events.UnitCheck.EventsType import EventsType
from agent.manager.DbusManager import get_sysd_manager, get_sys_bus
from agent.scheduler import Scheduler


def check_status(status):
    load_state = status["LoadState"]
    active_state = status["ActiveState"]
    exec_start = status["ExecStart"]
    status_code = exec_start[0][9]
    if load_state == 'loaded' and active_state == 'inactive':
        if status_code == 143:
            Scheduler.schedule_function(restart_unit)


def restart_unit():
    get_sysd_manager(bus=get_sys_bus()).RestartUnit("artemis.service", "replace",
                                                    reply_handler=lambda job: print(job),
                                                    error_handler=lambda e: print(e))
    return False


class RestartServiceSink:

    def __init__(self, publisher, name='RestartServiceSink'):
        properties_listener = Subscriber(name)
        properties_listener.subscribe(EventsType.ReadsDone, publisher, callback=check_status)


