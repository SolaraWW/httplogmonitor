def parse_datetime(x):
    '''
    Parses datetime with timezone formatted as:
        `[day/month/year:hour:minute:second zone]`

    Example:
        `>>> parse_datetime('13/Nov/2015:11:45:42 +0000')`
        `datetime.datetime(2015, 11, 3, 11, 45, 4, tzinfo=<UTC>)`

    Due to problems parsing the timezone (`%z`) with `datetime.strptime`, the 
    timezone will be obtained using the `pytz` library.

    Taken from: http://blog.mmast.net/read-apache-access-log-pandass
    '''
    import pytz
    from datetime import datetime
    dt = datetime.strptime(x[0:-6], '%d/%b/%Y:%H:%M:%S')
    dt_tz = int(x[-6:-3])*60+int(x[-3:-1])    
    return dt.replace(tzinfo=pytz.FixedOffset(dt_tz))
