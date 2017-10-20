# -*- coding: utf-8 -*-
import re
import time

def encode_publish_time(initial_publish_time):
    time_t = None
    if re.search("今天 \d{2}:\d{2}", initial_publish_time):
        time_t = time.strftime('%Y-%m-%d ', time.localtime(time.time())) + re.search("今天 (\d{2}:\d{2})",
                                                                                     initial_publish_time).group(1)
    elif re.search("\d{2}月\d{2}日 \d{2}:\d{2}", initial_publish_time):
        time_t = time.strftime('%Y-', time.localtime(time.time())) + re.search("(\d{2}月\d{2}日 \d{2}:\d{2})",
                                                                               initial_publish_time).group(1)
        time_t = time_t.replace("月", "-").replace("日", "")
    elif re.search("\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", initial_publish_time):
        time_t = re.search("(\d{4}-\d{2}-\d{2} \d{2}:\d{2}):\d{2}", initial_publish_time).group(1)

    time_array = time.strptime(time_t, "%Y-%m-%d %H:%M")
    return int(time.mktime(time_array))


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass