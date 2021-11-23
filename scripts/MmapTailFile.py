import mmap
from concurrent.futures import ThreadPoolExecutor

io_pool_exc = ThreadPoolExecutor()

line = yield from loop.run_in_executor(io_pool_exc, f.readline)

def load_mmap_object(filename):
    def mmap_io_find_and_seek(filename):
        print("opening filename")
        with open(filename, mode="r", encoding="utf-8") as file_obj:
            return mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_READ)
            while True:
                data = f.readline()
            if data:
                return data
            yield from asyncio.sleep(PERIOD)


