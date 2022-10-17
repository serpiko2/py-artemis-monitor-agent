import logging

from source.asyn.jobs.RestartJob import RestartJob
from source.asyn.models.UnitProperties import UnitProperties
from source.config.MonitorConfig import MonitorConfig
from source.core.pubsub.EventsType import EventsType
from source.core.pubsub.Processor import Processor

class JobsEventHandler(Processor):

    logger = logging.getLogger(__name__)

    def __init__(self):
        super().__init__()
        self.subscriber.subscribe(EventsType.ReadsDone, self.publisher,
                                  callback=lambda unit_properties:
                                  self.monitor_handling_callback(unit_properties))
        self.subscriber.subscribe(EventsType.TriggerRestart, self.publisher,
                                  callback=lambda service_name:
                                  self.restart_handling_callback(service_name))

    @classmethod
    def restart_handling_callback(cls, service_name):
        cls.logger.info(f"Restarting unit={service_name}")
        RestartJob.restart_unit_non_blocking(service_name)

    @classmethod
    def monitor_handling_callback(cls, unit_properties: UnitProperties):
        if unit_properties.load_state == 'loaded' and unit_properties.active_state == 'active':
            cls.publisher.publish(EventsType.ProcessLogStart, "Service started, triggering Monitor process")
        elif not JobsEventHandler.check_user_interruption(unit_properties) \
                and MonitorConfig.restart_on_shutdown:
            cls.publisher.publish(EventsType.TriggerRestart, unit_properties.service_name)
        else:
            cls.publisher.publish(EventsType.ProcessLogStop, "Service stopped by user, doing nothing")

    @classmethod
    def check_user_interruption(cls, properties: UnitProperties):
        exec_start = properties.exec_start
        load_state = properties.load_state
        active_state = properties.active_state
        exec_codes = exec_start[0]
        status_code = exec_codes[len(exec_codes)-1]
        cls.logger.debug(f"load_state:{load_state}, "
                         f"active_state:{active_state}, "
                         f"status_code:{status_code}")
        if load_state == 'loaded' and active_state == 'inactive':
            if status_code == 143:
                return True
        return False
