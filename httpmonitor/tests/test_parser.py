import os
from httpmonitor.parser import parse_line, get_section


def test_apache():
    dirname, filename = os.path.split(os.path.abspath(__file__))
    fname = os.path.join(dirname, "../../data/apache_logs.txt")
    apache_lines = open(fname, "r").readlines()

    fname = os.path.join(dirname, "../../data/nginx_logs.txt")
    nginx_lines = open(fname, "r").readlines()
    
    line_0 = {'host': '83.149.9.216', 'user': '-', 'date': '17/May/2015:10:05:03 +0000', 'request': 'GET /presentations/logstash-monitorama-2013/images/kibana-search.png HTTP/1.1', "section": "/presentations/logstash-monitorama-2013", 'status': '200', 'size': '203023'}
    line_10 = {'host': '83.149.9.216', 'user': '-', 'date': '17/May/2015:10:05:46 +0000', 'request': 'GET /presentations/logstash-monitorama-2013/images/Dreamhost_logo.svg HTTP/1.1', "section": "/presentations/logstash-monitorama-2013", 'status': '200', 'size': '2126'}
    line_543 = {'host': '65.55.213.73', 'user': '-', 'date': '17/May/2015:15:05:44 +0000', 'request': 'GET /blog/tags/year%20review HTTP/1.1', "section": "/blog/tags", 'status': '200', 'size': '34590'}
    line_6543 = {'host': '115.112.233.75', 'user': '-', 'date': '19/May/2015:16:05:23 +0000', 'request': 'GET /presentations/logstash-puppetconf-2012/images/xkcd-perl.png HTTP/1.1', "section": "/presentations/logstash-puppetconf-2012", 'status': '200', 'size': '80663'}
    assert parse_line(apache_lines[0]) == line_0
    assert parse_line(apache_lines[10]) == line_10
    assert parse_line(apache_lines[543]) == line_543
    assert parse_line(apache_lines[6543]) == line_6543
    

    line_0 = {'host': '93.180.71.3', 'user': '-', 'date': '17/May/2015:08:05:32 +0000', 'request': 'GET /downloads/product_1 HTTP/1.1', "section": "/downloads/product_1", 'status': '304', 'size': '0', 'referer': '-', 'agent': 'Debian APT-HTTP/1.3 (0.8.16~exp12ubuntu10.21)'}
    line_42 = {'host': '91.239.186.133', 'user': '-', 'date': '17/May/2015:08:05:04 +0000', 'request': 'GET /downloads/product_2 HTTP/1.1', "section": "/downloads/product_2", 'status': '304', 'size': '0', 'referer': '-', 'agent': 'Debian APT-HTTP/1.3 (0.9.7.9)'}
    line_2717 = {'host': '5.39.64.195', 'user': '-', 'date': '18/May/2015:06:05:52 +0000', 'request': 'GET /downloads/product_2 HTTP/1.1', "section": "/downloads/product_2", 'status': '404', 'size': '338', 'referer': '-', 'agent': 'Debian APT-HTTP/1.3 (1.0.1ubuntu2)'}
    line_7654 = {'host': '31.31.75.239', 'user': '-', 'date': '20/May/2015:00:05:19 +0000', 'request': 'GET /downloads/product_1 HTTP/1.1', "section": "/downloads/product_1", 'status': '304', 'size': '0', 'referer': '-', 'agent': 'Debian APT-HTTP/1.3 (0.9.7.9)'}
    assert parse_line(nginx_lines[0], type_="extended") == line_0
    assert parse_line(nginx_lines[42], type_="extended") == line_42
    assert parse_line(nginx_lines[2717], type_="extended") == line_2717
    assert parse_line(nginx_lines[7654], type_="extended") == line_7654


def test_get_section():
    assert get_section('GET / HTTP/1.1') == "/"
    assert get_section('GET /downloads HTTP/1.1') == "/downloads"
    assert get_section('GET /downloads/product_1 HTTP/1.1') == "/downloads/product_1"
    assert get_section('GET /downloads/product_1/1/1/1/1/1/1/1 HTTP/1.1') == "/downloads/product_1"
