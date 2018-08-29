import os
import time
import click
import asyncio
import pandas as pd

from httpmonitor.parser import parse_line


data = []
new_data = []

interval = 120
alert_limit = 10  # per second

interval = 1
alert_limit = 10  # per second


async def tail_file(fname):
    global new_data

    with open(fname, "r") as f:
        f.seek(0, os.SEEK_END)  # Go to the end of file
        while True:
            line = f.readline()
            if line:
                # print(line)
                new_data.append(parse_line(line))
            else:
                await asyncio.sleep(interval / 10)


async def process_data():
    global data, new_data
    while True:
        await asyncio.sleep(interval)
        data = new_data
        new_data = []
        print("Process", len(data))


loop = asyncio.get_event_loop()
try:
    # fname = "/var/log/access.log"
    fname = "./scratch/logs.txt"
    asyncio.ensure_future(tail_file(fname))
    asyncio.ensure_future(tail_file(fname))
    asyncio.ensure_future(tail_file(fname))
    asyncio.ensure_future(process_data())
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print("Closing Loop")
    loop.close()


# @click.command()
# @click.option("--file", "filename", default="logs.txt", type=click.Path())
# @click.option("--interval", default=10, help="Interval (seconds)")
# @click.option("--threshold", default=20, help="Threshhold (records)")
# def main(filename, n, mean, std):



# if __name__ == '__main__':
#     filename = sys.argv[1]
#     nlines = int(sys.argv[2])
#     tail_file(filename, nlines)


# if __name__ == "__main__":
#     main()
