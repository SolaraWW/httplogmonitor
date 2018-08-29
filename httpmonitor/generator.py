import os
import time
import click
import random


dirname, filename = os.path.split(os.path.abspath(__file__))
fname = os.path.join(dirname, "../data/apache_logs.txt")
apache_lines = open(fname, "r").readlines()


@click.command()
@click.option("--file", "file_", default="logs.txt", type=click.Path())
@click.option("--n", default=5, help="Number of items to write")
@click.option("--mean", default=0.5, help="Mean")
@click.option("--std", default=0.1, help="STD")
def main(file_, n, mean, std):
    with open(file_, "w+") as f:
        while True:
            for _ in range(n):
                i = random.randint(0, len(apache_lines))
                line = apache_lines[i].strip()
                click.echo(f"Writting: {line}")
                f.write(line + "\n")
            f.flush()
            time.sleep(random.normalvariate(mean, std))


if __name__ == "__main__":
    main()
