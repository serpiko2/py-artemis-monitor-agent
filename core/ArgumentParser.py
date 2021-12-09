import argparse


class ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', '-m', help="the mode on out it will run, accept ASYNC or SYNC. ASYNC IS A WIP",
                        type=str)
    parser.add_argument('--service', '-s', help="the service name, comprehensive of .service", type=str)

    @staticmethod
    def get_parser():
        return ArgumentParser.parser
