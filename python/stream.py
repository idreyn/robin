import numpy as np
import alsaaudio as aa
import time

class Stream(object):
    def __init__(self, device, is_input):
        self.device = device
        self.is_input = is_input
        self.pcm = aa.PCM(
            type=aa.PCM_CAPTURE, #if is_input else aa.PCM_PLAYBACK,
            mode=aa.PCM_NORMAL,
            cardindex=1 #device=self.device.name
        )
        self.pcm.setrate(device.rate)
        self.pcm.setchannels(device.channels)
        self.pcm.setformat(aa.PCM_FORMAT_S16_LE)
        self.pcm.setperiodsize(device.periodsize)
        while True:
            r = self.read()
            if len(r) < 500:
                print len(r)

    def read(self):
      length, data = self.pcm.read()
      return np.fromstring(data, dtype=np.int16)

class SampleBuffer(object):
	def __init__(self, channels):
		self.queue = []
                self.channels = channels

        def size(self):
            return sum([len(s) for s in self.queue])

	def put(self, sample):
		self.queue.append(np.copy(sample))

	def has(self):
		return len(self.queue) > 0

	def get_chunk(self):
		return self.queue.pop(0)

        def get_samples(self, length=None):
            pointer = 0
            if length is None:
                length = self.size()
            buff = np.zeros((length, self.channels))
            while pointer < length:
                if not len(self.queue):
                        break
                else:
                    sample = self.queue[0]
                    take = min(length - pointer, len(sample))
                    buff[pointer : pointer + take, :] = sample[0:take, :]
                    self.queue[0] = sample[take:, :]
                    pointer = pointer + take
                    if not len(self.queue[0]):
                            self.queue.pop(0)
                            return buff
