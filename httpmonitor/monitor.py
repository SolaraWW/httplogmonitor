import os
import time
import click
import asyncio
import datetime
import pandas as pd

from httpmonitor.utils import parse_datetime
from httpmonitor.parser import parse_line


async def tail_file(queue, alert_queue, fname, read_interval):
    with open(fname, "r") as file:
        file.seek(0, os.SEEK_END)  # Go to the end of file
        while True:
            curr_position = file.tell()
            line = file.readline()
            if line:
                await queue.put(parse_line(line))
                await alert_queue.put(1)  # This Queue only needs to know that there is an item there
            else:
                file.seek(curr_position)
                await asyncio.sleep(read_interval)


async def alert_handler(queue, alert_queue_msg, interval=120, threshold=10, current_alert=False, stop=False):
    while True:
        if current_alert and queue.qsize() < threshold:
            print(queue.qsize())
            alert = {"type": "recover", "hits": queue.qsize(), "time": datetime.datetime.now()}
            current_alert = False
            await alert_queue_msg.put(alert)
        if queue.qsize() > threshold:
            alert = {"type": "alert", "hits": queue.qsize(), "time": datetime.datetime.now()}
            current_alert = True
            await alert_queue_msg.put(alert)
        queue._queue.clear()

        if stop:
            break
        await asyncio.sleep(interval)


async def process(queue, queue_alert_msg, interval):
    alerts = []
    
    while True:
        await asyncio.sleep(interval)
        data = []
        while not queue.empty():
            item = await queue.get()
            data.append(item)
        while not queue_alert_msg.empty():
            msg = await queue_alert_msg.get()
            alerts.append(msg)
        # click.echo("Process: {n}".format(n=len(data)))
        
        click.clear()
        if len(data) >= 1:
            df = pd.DataFrame.from_records(data)
            df['count'] = df.groupby('section')['section'].transform('count')
            df = df.sort_values("count", ascending=False)
            df["date"] = df.date.apply(parse_datetime)
            click.clear()
            click.echo(f"Top 30 sections in the last {interval} seconds:")
            df_show = df[["section", "size", "status", "host", "date", "count"]][:30].reset_index()
            click.echo(df_show)
        else:
            click.echo("No new events")
        
        click.echo("\n\n")
        click.echo("Last 10 alerts messages:")
        for alert in alerts[-10:]:
            if alert["type"] == "alert":
                value = alert["hits"]
                time = alert["time"]
                click.echo(f"High traffic generated an alert - hits = {value}, triggered at {time}")
            else:
                value = alert["hits"]
                time = alert["time"]
                click.echo(f"High traffic went down at {time} with: {value} hits")


@click.command()
@click.option("--file", "-f", "filenames", default=["/var/log/access.log"], type=click.Path(), multiple=True)
@click.option("--interval", "-i", default=10, help="Interval (seconds)")
@click.option("--alert-interval", "-a", "alert_interval", default=120, help="Threshhold (records)")
@click.option("--threshold", "-t", default=1200, help="Threshhold (records)")
def main(filenames, interval, threshold, alert_interval):
    click.echo(f"Starting to read: {filenames} in {interval} seconds")

    try:
        read_interval = min(1, interval / 10)

        loop = asyncio.get_event_loop()
        queue = asyncio.Queue(loop=loop)
        queue_alert = asyncio.Queue(loop=loop)
        queue_alert_msg = asyncio.Queue(loop=loop)


        for fname in filenames:
            asyncio.ensure_future(tail_file(queue, queue_alert, fname, read_interval=read_interval))
        asyncio.ensure_future(alert_handler(queue_alert, queue_alert_msg, interval=alert_interval, threshold=threshold))
        asyncio.ensure_future(process(queue, queue_alert_msg, interval=interval))
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print("Closing Loop")
        loop.close()


if __name__ == "__main__":
    main()
