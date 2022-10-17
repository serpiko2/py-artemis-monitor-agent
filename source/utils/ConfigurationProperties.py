import configparser
from source.utils.ArgumentParser import ArgumentParser


class ConfigurationProperties:
    config = configparser.RawConfigParser()
    config.read(ArgumentParser.get_parsed_args().config)

    @classmethod
    def get(cls, sect, key):
        return cls.config.get(sect, key)
