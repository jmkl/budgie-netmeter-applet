import os
import psutil
import time
import copy
from threading import Thread


class MThread(Thread):

    def __init__(self, parent):
        Thread.__init__(self)
        self.parent = parent
        self.data = 0
        self.nmtext = NetMeterText()

    def update(self):
        self.data = self.nmtext.fetch()
        return self.data

    def run(self):
        while self.parent.alive.isSet():
            self.parent.update(self.update())
            time.sleep(1)


class NetMeterText(object):

    def __init__(self):
        self.last = [0, 0]

    def format(self, data):
        d = [cv(data[0]), cv(data[1])]
        return d

    def fetch(self):
        net = psutil.net_io_counters(pernic=True)
        curr = [0, 0]
        for _, io in net.items():
            curr[0] += io.bytes_recv
            curr[1] += io.bytes_sent
        temp = copy.deepcopy(curr)
        curr[0] -= self.last[0]
        curr[1] -= self.last[1]
        self.last = temp
        return self.format(curr)
#
#   return the like n xB
#


def cv(_num, suffix='B'):
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(_num) < 1024:
            strnum = "%3.0f" % (_num)
            return (strnum.strip(), unit + suffix)
        _num /= 1024.0
    return (_num.strip(), 'Y' + suffix)
