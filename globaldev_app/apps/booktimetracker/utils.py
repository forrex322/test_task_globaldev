from datetime import datetime, time


def time_diff(time_str1, time_str2):
    """
    Helpful method for calculation duration of readin session.
    """
    t1 = datetime.strptime(time_str1, "%H:%M")
    t2 = datetime.strptime(time_str2, "%H:%M")
    dt = abs(t2 - t1)
    return time(dt.seconds // 3600, (dt.seconds // 60) % 60).strftime("%H:%M")
