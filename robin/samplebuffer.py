import time
import bisect
import numpy as np
from multiprocessing import Manager


class SampleBuffer(object):

    def __init__(self, channels, period_capacity=500):
        self.manager = Manager()
        self.queue = []
        self.times = []
        self.channels = channels
        self.period_capacity = period_capacity

    def time_range(self):
        return (self.times[0], self.times[-1])

    def put(self, sample):
        self.queue.append(np.copy(sample))
        self.times.append(time.time())
        if len(self.queue) > self.period_capacity:
            self.shift()

    def shift(self, ln=1):
        res = self.queue[0:ln]
        self.queue = self.queue[ln:]
        self.times = self.times[ln:]
        return res

    def pointer_for_time(self, time, start_limit=0, end_limit=None):
        if not end_limit:
            end_limit = len(self.times)
        midpoint = (start_limit + end_limit) / 2

    def get_samples(self, length, start_time=None):
        offset = 0 if start_time is None \
            else bisect.bisect_left(self.times, start_time)
        self.shift(offset)
        pointer = 0
        buff = np.zeros((length, self.channels))
        i = 0
        while pointer < length:
            i = i + 1
            if not len(self.queue):
                break
            else:
                sample = self.queue[0]
                take = min(length - pointer, len(sample))
                t0 = time.time()
                buff[pointer: pointer + take, :] = sample[0:take, :]
                self.queue[0] = sample[take:, :]
                pointer = pointer + take
                if not len(self.queue[0]):
                    self.shift()
        return buff
