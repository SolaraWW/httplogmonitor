# HTTP log Monitor

HTTP log monitor

## Problem

Consume an actively written-to w3c-formatted HTTP access log (https://en.wikipedia.org/wiki/Common_Log_Format). It should default to reading /var/log/access.log and be overridable.
Example log lines:

```
127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 200 1234
127.0.0.1 - jill [09/May/2018:16:00:41 +0000] "GET /api/user HTTP/1.0" 200 1234
127.0.0.1 - frank [09/May/2018:16:00:42 +0000] "GET /api/user HTTP/1.0" 200 1234
127.0.0.1 - mary [09/May/2018:16:00:42 +0000] "GET /api/user HTTP/1.0" 200 1234
```

- Display stats every 10s about the traffic during those 10s: the sections of the web site with the most hits, as well as interesting summary statistics on the traffic as a whole. A section is defined as being what's before the second '/' in the path. For example, the section for "http://my.site.com/pages/create” is "http://my.site.com/pages".
- Make sure a user can keep the app running and monitor the log file continuously
- Whenever total traffic for the past 2 minutes exceeds a certain number on average, add a message saying that “High traffic generated an alert - hits = {value}, triggered at {time}”. The default threshold should be 10 requests per second and should be overridable.
- Whenever the total traffic drops again below that value on average for the past 2 minutes, print or displays another message detailing when the alert recovered.
- Write a test for the alerting logic.
- Explain how you’d improve on this application design.
- If you have access to a linux docker environment, we'd love to be able to docker build and run your project! If you don't though, don't sweat it. As an example:
 
```
FROM python:3
RUN touch /var/log/access.log # since the program will read this by default
WORKDIR /usr/src
ADD . /usr/src
ENTRYPOINT ["python", "main.py"]
```

## Solution

1. Python library structure including versioneer
1. Uses asyncio to manage the corrutines
1. Can read from multiple files configurable from arguments in the CLI
1. All values configurable from CLI arguments
1. Test for the alert system and other basic tests
1. Generate script to test. Generates events to a file randomly (normal distribution) from a sample file
1. Docker env

## How to an example

Create the local environment doing:

```
conda env create
```

Run tests:

```
make test
```

Build docker image using:

```
make build
```

Start the two generate script locally so one will generate two events per second (normal dist) and the other one 5 evens per seconds (normal dist)

```
## Generate two events every
python httpmonitor/generator.py --file ./scratch/log.txt -n 2
python httpmonitor/generator.py --file ./scratch/log2.txt -n 5
```

Run the monitor:
- Reading two files (`/var/log/access2.log` -> `./scratch/log.txt` and `/var/log/access.log` -> `./scratch/log2.txt`)
- Interval of 3 seconds 
- Alert threshold of 10 events every 5ss

```
make devtest
```

At this point the program will start printing some alert. Stop the generator with `-n 5` and it will print a recover message.

## How to run it

To run it with the problem description defaults:

- Reading from a from a single file (`/var/log/access.log`) where that file is mounted to `./scratch/log.txt` in the host 
- Update interval of 10 seconds
- Alert threshold of 1200 events every 120s

```
make run
```


## Improvements

1. Tests can be better as they just check basic cases
1. Interface is quite basic and it just clears the terminal every X seconds. It should use something more advanced like `ncurses`
1. Organization of the library can be better and use entrypoints instead of calling the scripts directly
1. Add tests that generate script (or something similar) to have more real integration testing
