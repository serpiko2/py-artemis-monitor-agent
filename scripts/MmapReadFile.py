import mmap
import asyncio
import re
import sys
from datetime import datetime, timedelta

format_string = "%Y-%m-%d %H:%M:%S,%f"

format_log_pattern = "%d %-5p [%c] %s%E%n"

timestamp_regex = r'(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\,\d{3})\s'

log_level_regex = r'(\w*)\s*'

logging_class_regex = r'(\[(\w*).+\])'

message_regex = r'.(.*)'

regex_pattern = timestamp_regex + log_level_regex + logging_class_regex + message_regex


def seek_around_marker(line: str, marker: str, pre: str, post: str):
    date_match = re.search(regex_pattern, line).group(1)
    print(date_match)


def seek_seconds_around_timestamp(timestamp: str, pre: int, post: int):
    date_object = datetime.strptime(timestamp, format_string)
    print(date_object)
    past = date_object - timedelta(seconds=pre)
    future = date_object + timedelta(seconds=post)
    print(f"now: {date_object}, past: {past}, future: {future}")


def check_codes(line):
    if "AMQ224097" in line:
        if "FAILED TO SETUP the JDBC Shared State NodeId" in line:
            print("Connection to database failed while setting up Jdbc Shared State NodeId, restarting service")
            print("Connection to database failed while setting up Jdbc Shared "
                  "State NodeId, restarting service")
            sys.exit(1)
    elif "AMQ221043" in line:
        print("Artemis initialized correctly")
        sys.exit(0)
    else:
        print("Logs not founds?")
        sys.exit(0)


def mmap_io_find_and_seek(filename):
    print("opening filename")
    with open(filename, mode="r", encoding="utf-8") as file_obj:
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_obj:
            for line in iter(mmap_obj.readline, b""):
                check_codes(line.decode("utf-8").rstrip())


if __name__ == '__main__':
    seek_around_marker("2021-11-23 00:24:32,033 INFO  [org.apache.activemq.hawtio.plugin.PluginContextListener] "
                       "Destroyed artemis-plugin plugin", format_log_pattern, 0, 0)
    # seek_seconds_around_timestamp("2021-11-23 15:06:05,450", 0, 0)
    # mmap_io_find_and_seek(filename="test.file")
