import mmap
from datetime import datetime

from _utils.parser.LogParser import LogGroups, LogPatterns
from _utils.parser.StringParser import Parser


def seek_marker(line: str, marker: LogGroups):
    log_groups = Parser.parse_string(line, clazz=LogGroups, regex=LogPatterns.regex_pattern)
    if marker.partial_eq(log_groups):
        return log_groups


def seek_timestamp(line: str, timestamp: datetime):
    return seek_marker(line, LogGroups(timestamp=timestamp))


def check_codes(message):
    if "AMQ224097" in message:
        if "FAILED TO SETUP the JDBC Shared State NodeId" in message:
            print("Connection to database failed while setting up Jdbc Shared State NodeId, restarting service")
            print("Connection to database failed while setting up Jdbc Shared "
                  "State NodeId, restarting service")
    elif "AMQ221043" in message:
        print("Artemis initialized correctly")
    else:
        print("Logs not founds?")


def read_file(file, callback, *args):
    print("read_file")
    for line in iter(file.readline, b""):
        print("read_file args", args)
        yield callback(line.decode("utf-8").rstrip(), *args)


def mmap_io_find_and_open(filename):
    print("opening filename")
    with open(filename, mode="r", encoding="utf-8") as file_obj:
        return mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_READ)


if __name__ == '__main__':
    test_file = mmap_io_find_and_open(filename="test_file.log")
    ts = datetime.strptime("2021-11-23 00:24:32,033", LogPatterns.timestamp_pattern)
    print("reading timestamp:", ts)
    for x in read_file(test_file, seek_timestamp, ts):
        check_codes(x.message)
    # seek_around_marker("2021-11-23 00:24:32,033 INFO  [org.apache.activemq.hawtio.plugin.PluginContextListener] "
    #                    "Destroyed artemis-plugin plugin", format_log_pattern, 0, 0)
    # seek_seconds_around_timestamp("2021-11-23 15:06:05,450", 0, 0)
    # mmap_io_find_and_seek(filename="test.file")
