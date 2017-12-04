import datetime
__all__ = ['dumps', 'loads', 'loads_utf8']


try:
    import json
except ImportError:
    import simplejson as json


class JSONDateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        else:
            return json.JSONEncoder.default(self, obj)


def datetime_decoder(d):
    if isinstance(d, list):
        pairs = enumerate(d)
    elif isinstance(d, dict):
        pairs = d.items()
    result = []
    for k, v in pairs:
        if isinstance(v, str):
            try:
                # The %f format code is only supported in Python >= 2.6.
                # For Python <= 2.5 strip off microseconds
                # v = datetime.datetime.strptime(v.rsplit('.', 1)[0],
                #     '%Y-%m-%dT%H:%M:%S')
                # v = datetime.datetime.strptime(v, '%Y-%m-%dT%H:%M:%S.%f')
                v = datetime.datetime.strptime(v, '%Y-%m-%dT%H:%M:%S')
            except ValueError:
                try:
                    v = datetime.datetime.strptime(v, '%Y-%m-%d')
                except ValueError:
                    try:
                        v = datetime.datetime.strptime(v, '%H:%M:%S').time()
                    except ValueError:
                        pass
        elif isinstance(v, (dict, list)):
            v = datetime_decoder(v)
        result.append((k, v))
    if isinstance(d, list):
        return [x[1] for x in result]
    elif isinstance(d, dict):
        return dict(result)


def dumps(obj):
    return json.dumps(obj, cls=JSONDateTimeEncoder)


def loads(obj):
    return json.loads(obj, object_hook=datetime_decoder)


def loads_utf8(obj: bytes) -> dict:
    return loads(obj.decode('utf-8'))

# how to use:
#
# if __name__ == '__main__':
#     mytimestamp = datetime.datetime.utcnow()
#     mydate = datetime.date.today()
#     data = dict(
#         foo = 42,
#         bar = [mytimestamp, mydate],
#         date = mydate,
#         timestamp = mytimestamp,
#         struct = dict(
#             date2 = mydate,
#             timestamp2 = mytimestamp
#         )
#     )
#
#     print repr(data)
#     jsonstring = dumps(data)
#     print jsonstring
#     print repr(loads(jsonstring))
