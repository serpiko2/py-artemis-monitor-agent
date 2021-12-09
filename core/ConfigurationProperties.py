import configparser


class ConfigurationProperties:

    config = configparser.RawConfigParser()
    config.read('config.properties')

    @staticmethod
    def get(sect, key):
        return ConfigurationProperties.config.get(sect, key)
