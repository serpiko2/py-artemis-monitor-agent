import logging
import time
import os
import asyncio

logger = logging.getLogger("TailFile")


def log_line(line):
    logger.warning(line)


def follow(file, callback=log_line):
    file.seek(0, os.SEEK_END)
    while True:
        line = file.readline()
        if not line:
            continue
        callback(line)

# mmap - load file in mem