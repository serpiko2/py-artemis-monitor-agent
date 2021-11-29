from events.AsyncScheduler import AsyncScheduler
from events.jobs.GetProperty import GetPropertyJob
from events.models.PropertiesServiceParameters import PropertiesServiceParameters
from events.pubsub.Events import Publisher, Subscriber
from events.pubsub.EventsType import EventsType

context = {}


class ServiceContextRestart:
    active_state = None
    load_state = None
    exec_start = None


def _schedule_retrieves(publisher, service_properties):
    active_state_job = GetPropertyJob(
            publisher=publisher,
            event=EventsType.Jobs.ActiveStateRead,
            params=PropertiesServiceParameters(service_properties,
                                               'org.freedesktop.systemd1.Unit', 'ActiveState'),
            delay=0,
            loop=False)
    load_state_job = GetPropertyJob(
            publisher=publisher,
            event=EventsType.Jobs.LoadStateRead,
            params=PropertiesServiceParameters(service_properties,
                                               'org.freedesktop.systemd1.Unit', 'LoadState'),
            delay=0,
            loop=False)
    exec_start_job = GetPropertyJob(
            publisher=publisher,
            event=EventsType.Jobs.ExecStartRead,
            params=PropertiesServiceParameters(service_properties,
                                               'org.freedesktop.systemd1.Service', 'ExecStart'),
            delay=0,
            loop=False)
    AsyncScheduler.schedule_jobs(active_state_job, load_state_job, exec_start_job)


class StatusAwareProcessor:

    def __init__(self,
                 service_name: str,
                 publisher: Publisher,
                 listener: Subscriber
                 ):
        self.service_name = service_name
        self.listener = listener
        self.publisher = publisher
        self._setup_subscriber()
        context[service_name, ServiceContextRestart.__name__] = None

    def _setup_subscriber(self):
        self.listener.subscribe(
            EventsType.Jobs.UnitFound, self.publisher,
            callback=lambda message:
            _schedule_retrieves(self.publisher, message)
        )
        self.listener.subscribe(
            EventsType.Jobs.ActiveStateRead, self.publisher,
            callback=lambda message:
            self._set_active_state(message)._are_checks_done()
        )
        self.listener.subscribe(
            EventsType.Jobs.LoadStateRead, self.publisher,
            callback=lambda message:
            self._set_load_state(message)._are_checks_done()
        )
        self.listener.subscribe(
            EventsType.Jobs.ExecStartRead, self.publisher,
            callback=lambda message:
            self._set_exec_start(message)._are_checks_done()
        )
        self.listener.subscribe(
            EventsType.Jobs.ReadsDone, self.publisher,
            callback=lambda message:
            self.check_status(message)
        )

    def _set_active_state(self, data):
        context.get(self.service_name,
                    ServiceContextRestart.__name__).active_state = data
        return self

    def _set_load_state(self, data):
        context.get(self.service_name,
                    ServiceContextRestart.__name__).load_state = data
        return self

    def _set_exec_start(self, data):
        context.get(self.service_name,
                    ServiceContextRestart.__name__).exec_start = data
        return self

    def _are_checks_done(self):
        params = context.get(self.service_name)
        if params.exec_start and params.load_state and params.active_state:
            self.publisher.publish(EventsType.Jobs.ReadsDone,
                                   {"LoadState": params.load_state,
                                    "ActiveState": params.active_state,
                                    "ExecStart": params.exec_start})

    def check_status(self, event):
        print("check status")
        load_state = event["LoadState"]
        active_state = event["ActiveState"]
        exec_start = event["ExecStart"]
        status_code = exec_start[0][9]
        print(f"service:, load_state:{load_state}, "
              f"active_state:{active_state}, status_code:{status_code}")
        if load_state == 'loaded' and active_state == 'inactive':
            if status_code == 143:
                self.publisher.publish(EventsType.Jobs.TriggerRestart, self.service_name)
