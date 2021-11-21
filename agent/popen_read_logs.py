import sys
import subprocess
import select
from os import path
import logging
import dbus

log_mapping = {"INFO": 20, "DEBUG": 10, "WARN": 30, "ERROR": 40, "CRITICAL": 50}

bus = dbus.SystemBus()
proxy = bus.get_object('org.freedesktop.DBus', '/org/freedesktop/systemd1')

args = sys.argv
artemis_log_file_path = str(args[1])

logging.basicConfig(filename="amq-agent-control.log")
logger = logging.getLogger("amq-agent-control")
tailArgs = ["tail", "-F", "-n", "1"]

print(
    str.format("Agent Configurations: "
               "popenArgs={popenArgs}, "
               "artemis_log_file_path={logPath}, "
               "logging_level={logPath}",
               popenArgs=tailArgs, logPath=artemis_log_file_path)
)

logger.info(
    str.format("Agent Configurations: "
               "popenArgs={popenArgs}, artemis_log_file_path={logPath}",
               popenArgs=tailArgs, logPath=artemis_log_file_path)
)

if not path.isfile(artemis_log_file_path):
    print("Error on args[0], artemis log file not found")
    logger.error("Error on args[1], artemis log file not found, path=[%s]",
                 artemis_log_file_path)
else:
    tailArgs.append(artemis_log_file_path)
f = subprocess.Popen(tailArgs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
p = select.poll()
p.register(f.stdout)
logger.debug("subprocess registered")

if p.poll(1):
    s = f.stdout.readline().decode("utf-8")

while True:
    if p.poll(1):
        s = f.stdout.readline().decode("utf-8")
        if "AMQ224097" in s:
            if "FAILED TO SETUP the JDBC Shared State NodeId" in s:
                print("Connection to database failed while setting up Jdbc Shared State NodeId, restarting service")
                logger.error("Connection to database failed while setting up Jdbc Shared "
                             "State NodeId, restarting service")
                sys.exit(1)
        elif "AMQ221043" in s:
            print("Artemis initialized correctly")
            logger.info("Artemis initialized correctly")
            sys.exit(0)
