import logging


def configure_logger():
    log_mapping = {"INFO": 20, "DEBUG": 10, "WARN": 30, "ERROR": 40, "CRITICAL": 50}
    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        filename="monitor.log",
                        level=log_mapping.get("DEBUG"))
