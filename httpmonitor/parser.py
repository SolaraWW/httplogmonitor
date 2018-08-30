import re

REGEX_COMMON_LOG = '([^ ]*) ([^ ]*) ([^ ]*) \[([^]]*)\] "([^"]*)" ([^ ]*) ([^ ]*)'
REGEX_EXTENDED_COMMON_LOG = '([^ ]*) ([^ ]*) ([^ ]*) \[([^]]*)\] "([^"]*)" ([^ ]*) ([^ ]*) "([^"]*)" "([^"]*)"' # extensions

common_log_pattern = re.compile(REGEX_COMMON_LOG)
extended_common_log_pattern = re.compile(REGEX_EXTENDED_COMMON_LOG)


def parse_line(line, type_='common'):
    """
    Parameters
    ----------
        line: String
        type: ('common' or 'extended'). Default (also if it doesnt match) is 'common'
    """
    data = {}

    if type_ == 'extended':
        match = extended_common_log_pattern.match(line)
        if match:
            host, ignore, user, date, request, status, size, referer, agent = match.groups()
            data = {"host": host, "user": user, "date": date, "request": request, "status": status, "size": size, "referer": referer, "agent": agent}
    else:
        match = common_log_pattern.match(line)
        if match:
            host, ignore, user, date, request, status, size = match.groups()
            data = {"host": host, "user": user, "date": date, "request": request, "status": status, "size": size}

    data["section"] = get_section(data["request"])
    return data

def get_section(request):
    """
    Get a section (what's before the second '/' in the path) from a request

    Return: Tuple of: (method(GET, POST...) , section)
    """
    method, path, http_ver = request.split(" ")
    paths = path.split("/")
    max_ = min([len(paths), 3])
    section = "/".join(paths[0:max_])
    return section.rstrip("/") or "/"
