#from requests_aws4auth
def parse_date(date_str):
    """
    Check if date_str is in a recognised format and return an ISO
    yyyy-mm-dd format version if so. Raise DateFormatError if not.

    Recognised formats are:
    * RFC 7231 (e.g. Mon, 09 Sep 2011 23:36:00 GMT)
    * RFC 850 (e.g. Sunday, 06-Nov-94 08:49:37 GMT)
    * C time (e.g. Wed Dec 4 00:00:00 2002)
    * Amz-Date format (e.g. 20090325T010101Z)
    * ISO 8601 / RFC 3339 (e.g. 2009-03-25T10:11:12.13-01:00)

    date_str -- Str containing a date and optional time

    """
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug',
              'sep', 'oct', 'nov', 'dec']
    formats = {
        # RFC 7231, e.g. 'Mon, 09 Sep 2011 23:36:00 GMT'
        r'^(?:\w{3}, )?(\d{2}) (\w{3}) (\d{4})\D.*$':
            lambda m: '{}-{:02d}-{}'.format(
                                      m.group(3),
                                      months.index(m.group(2).lower())+1,
                                      m.group(1)),
        # RFC 850 (e.g. Sunday, 06-Nov-94 08:49:37 GMT)
        # assumes current century
        r'^\w+day, (\d{2})-(\w{3})-(\d{2})\D.*$':
            lambda m: '{}{}-{:02d}-{}'.format(
                                        str(datetime.date.today().year)[:2],
                                        m.group(3),
                                        months.index(m.group(2).lower())+1,
                                        m.group(1)),
        # C time, e.g. 'Wed Dec 4 00:00:00 2002'
        r'^\w{3} (\w{3}) (\d{1,2}) \d{2}:\d{2}:\d{2} (\d{4})$':
            lambda m: '{}-{:02d}-{:02d}'.format(
                                          m.group(3),
                                          months.index(m.group(1).lower())+1,
                                          int(m.group(2))),
        # x-amz-date format dates, e.g. 20100325T010101Z
        r'^(\d{4})(\d{2})(\d{2})T\d{6}Z$':
            lambda m: '{}-{}-{}'.format(*m.groups()),
        # ISO 8601 / RFC 3339, e.g. '2009-03-25T10:11:12.13-01:00'
        r'^(\d{4}-\d{2}-\d{2})(?:[Tt].*)?$':
            lambda m: m.group(1),
    }

    out_date = None
    for regex, xform in formats.items():
        m = re.search(regex, date_str)
        if m:
            out_date = xform(m)
            break
    if out_date is None:
        raise DateFormatError
    else:
        return out_date
