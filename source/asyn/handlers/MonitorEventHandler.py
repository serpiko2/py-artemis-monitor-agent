import logging

from source.asyn.processors.MonitorEventProcessor import MonitorEventProcessor
from source.asyn.handlers.runnable.MonitorLogFileRunner import MonitorLogFileRunner
from source.config.MonitorConfig import MonitorConfig


class MonitorEventHandler(MonitorEventProcessor):
    logger = logging.getLogger(__name__)

    def __init__(self):
        super().__init__(self.monitor_start, self.monitor_stop)
        self.log_file_process = MonitorLogFileRunner(fail_strings=MonitorConfig.fail_strings,
                                                     success_strings=MonitorConfig.success_strings,
                                                     file_path=MonitorConfig.file_path,
                                                     service_name=MonitorConfig.service_name,
                                                     poll_rate=MonitorConfig.poll_rate)

    def monitor_start(self):
        self.log_file_process.start()

    def monitor_stop(self):
        self.log_file_process.stop()
