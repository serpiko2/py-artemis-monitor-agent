from _agent.events.Events import Publisher, Subscriber
from _agent.events.EventsType import EventsType
from _agent.jobs.GetProperty import GetPropertyJob, Properties, Interfaces
from _agent.models.PropertiesServiceParameters import PropertiesServiceParameters
from _agent.scheduler import Scheduler


def _schedule_retrieves(publisher, service_properties):
    active_state_job = GetPropertyJob(
            publisher=publisher,
            event=EventsType.ActiveStateRead,
            params=PropertiesServiceParameters(service_properties,
                                               Interfaces.Unit,
                                               Properties.ActiveState),
            delay=0,
            loop=False)
    load_state_job = GetPropertyJob(
            publisher=publisher,
            event=EventsType.LoadStateRead,
            params=PropertiesServiceParameters(service_properties,
                                               Interfaces.Unit,
                                               Properties.LoadState),
            delay=0,
            loop=False)
    exec_start_job = GetPropertyJob(
            publisher=publisher,
            event=EventsType.ExecStartRead,
            params=PropertiesServiceParameters(service_properties,
                                               Interfaces.Service,
                                               Properties.ExecStart),
            delay=0,
            loop=False)
    Scheduler.schedule_jobs(active_state_job, load_state_job, exec_start_job)


class StatusAwareProcessor:

    def __init__(self,
                 service_name: str,
                 publisher: Publisher,
                 listener: Subscriber
                 ):
        self.service_name = service_name
        self.listener = listener
        self.publisher = publisher
        self.active_state = None
        self.load_state = None
        self.exec_start = None
        self._setup_subscriber()

    def _setup_subscriber(self):
        self.listener.subscribe(
            EventsType.UnitFound, self.publisher,
            callback=lambda message:
            _schedule_retrieves(self.publisher, message)
        )
        self.listener.subscribe(
            EventsType.ActiveStateRead, self.publisher,
            callback=lambda message:
            self._set_active_state(message)._are_checks_done()
        )
        self.listener.subscribe(
            EventsType.LoadStateRead, self.publisher,
            callback=lambda message:
            self._set_load_state(message)._are_checks_done()
        )
        self.listener.subscribe(
            EventsType.ExecStartRead, self.publisher,
            callback=lambda message:
            self._set_exec_start(message)._are_checks_done()
        )
        self.listener.subscribe(
            EventsType.ReadsDone, self.publisher,
            callback=lambda message:
            self.check_status(message)
        )

    def _set_active_state(self, data):
        self.active_state = data
        return self

    def _set_load_state(self, data):
        self.load_state = data
        return self

    def _set_exec_start(self, data):
        self.exec_start = data
        return self

    def _are_checks_done(self):
        if self.exec_start and self.load_state and self.active_state:
            self.publisher.publish(EventsType.ReadsDone,
                                   {Properties.LoadState: self.load_state,
                                    Properties.ActiveState: self.active_state,
                                    Properties.ExecStart: self.exec_start})

    def check_status(self, context):
        load_state = context["LoadState"]
        active_state = context["ActiveState"]
        exec_start = context["ExecStart"]
        status_code = exec_start[0][9]
        print(f"service={self.service_name}, status=[load_state={load_state}, "
              f"active_state={active_state}, status_code={status_code}]")
        if load_state == 'loaded' and active_state == 'inactive':
            if status_code == 143:
                self.publisher.publish(EventsType.TriggerRestart, self.service_name)
