import configparser

config = configparser.RawConfigParser()
config.read('config.properties')


def get(sect, key):
    return config.get(sect, key)
