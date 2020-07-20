import time
import datetime as dte
from datetime import datetime


class Timer(object):

    def __init__(self):

        self.localtimer = time.localtime(time.time())
        self.start_timer = None
        self.end_timer = None

    def get_time(self):
        return "{}:{}".format(self.localtimer.tm_hour, self.localtimer.tm_min)

    def get_year(self):
        return "{}".format(self.localtimer.tm_year)

    def get_day(self):
        return "{}".format(self.localtimer.tm_mday)

    def get_month(self):
        return "{}".format(self.localtimer.tm_mon)

    def get_min(self):
        return "{}".format(self.localtimer.tm_min)

    def get_hour(self):
        return "{}".format(self.localtimer.tm_hour)

    def get_sec(self):
        return "{}".format(self.localtimer.tm_sec)

    def get_datetime(self, local_time):
        return int("{}".format(local_time.tm_year)), int("{}".format(local_time.tm_mon)), int(
            "{}".format(local_time.tm_mday)), int("{}".format(local_time.tm_hour)), int("{}".format(local_time.tm_min)), int("{}".format(local_time.tm_sec))

    def start_time(self):
        local_time = time.localtime(time.time())
        self.start_timer = dte.datetime(*self.get_datetime(local_time))

    def end_time(self):
        local_time = time.localtime(time.time())
        self.end_timer = dte.datetime(*self.get_datetime(local_time))

    def str_now(self):
        return datetime.now().strftime("%Y%m%d")

    def diff_btwn_date_in_sec(self):

        self.end_time()
        return ((self.end_timer - self.start_timer).total_seconds())
