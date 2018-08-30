FROM python:3

# Since the program will read this by default
RUN touch /var/log/access.log
RUN touch /var/log/access2.log

ADD ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

WORKDIR /usr/src
ADD . /usr/src
RUN pip install -e .

ENTRYPOINT ["python", "httpmonitor/monitor.py"]
