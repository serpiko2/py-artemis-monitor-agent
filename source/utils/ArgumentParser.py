import argparse


class ArgumentParser:

    _parser = argparse.ArgumentParser()
    _parser.add_argument('--config', '-c', help="the configuration file path",
                        type=str)

    @classmethod
    def get_parsed_args(cls):
        return cls._parser.parse_args()
