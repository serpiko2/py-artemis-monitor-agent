from source.utils.ConfigurationProperties import ConfigurationProperties


class MonitorConfig:

    service_name = ConfigurationProperties.get('MONITOR', 'service_name')
    restart_on_shutdown = bool(ConfigurationProperties.get('MONITOR', 'restart_on_shutdown'))
    poll_rate = int(ConfigurationProperties.get('MONITOR', 'poll_rate'))
    file_path = ConfigurationProperties.get('MONITOR', 'file_path')
    fail_strings = ConfigurationProperties.get('MONITOR', 'fail_tags').split(',')
    success_strings = ConfigurationProperties.get('MONITOR', 'success_tags').split(',')
