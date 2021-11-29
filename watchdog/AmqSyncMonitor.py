from datetime import datetime

from watchdog.steps import MmapReadFileStep
from watchdog.steps.GetPropertiesStep import GetPropertiesStep
from watchdog.steps.GetServiceStep import GetServiceStep
from watchdog.steps.RestartUnitStep import RestartUnitStep


class AmqSyncMonitor:

    @staticmethod
    def check_from_logs(path):
        test_file = MmapReadFileStep.mmap_io_find_and_open(filename="test_file.log")
        ts = datetime.now()
        print("reading timestamp:", ts)
        for x in MmapReadFileStep.read_file(test_file, MmapReadFileStep.seek_timestamp, ts):
            MmapReadFileStep.check_codes(x.message)

    @staticmethod
    def check_and_restart(service_name: str):
        unit = GetServiceStep.get_service(service_name)
        service_properties = GetPropertiesStep.get_service_properties(unit)
        properties = GetPropertiesStep.get_properties_for_restart(service_properties)
        restart_job = RestartUnitStep.restart_unit(properties, service_name)
        # reset restart counter
        return restart_job
