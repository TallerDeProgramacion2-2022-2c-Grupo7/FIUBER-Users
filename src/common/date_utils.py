from datetime import datetime

def get_datetime(timestamp):
    try:
        return datetime\
            .fromtimestamp(timestamp / 1000)\
            .strftime("%Y-%m-%d %H:%M:%S")
    except TypeError:
        return None
