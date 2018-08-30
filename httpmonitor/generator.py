import os
import time
import click
import random


dirname, filename = os.path.split(os.path.abspath(__file__))
fname = os.path.join(dirname, "../data/apache_logs.txt")
apache_lines = open(fname, "r").readlines()


@click.command()
@click.option("--file", "-f", "filename", default="/var/log/access.log ", type=click.Path())
@click.option("-n", default=1, help="Number of items to write")
@click.option("--mean", default=1, help="Mean (seconds)")
@click.option("--std", default=0.5, help="STD (seconds)")
def main(filename, n, mean, std):
    with open(filename, "w+") as f:
        while True:
            for _ in range(n):
                i = random.randint(0, len(apache_lines))
                line = apache_lines[i].strip()
                click.echo(f"Writting: {line}")
                f.write(line + "\n")
            f.flush()
            time.sleep(1)
            # time.sleep(abs(random.normalvariate(mean, std)))


if __name__ == "__main__":
    main()
