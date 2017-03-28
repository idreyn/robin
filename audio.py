from alsaaudio import ALSAAudioError

import time
import traceback
import threading
import sounddevice as sd

from stream import *
from record import *
from config import *
from util import *
from samplebuffer import *

def run_emit_thread(emit_stream, buffers, record_stream, record_buffer):
    period_size = emit_stream.device.period_size
    while True:
        """
        emit_stream.write_array(reduce(
            np.add,
            [b.get_samples(period_size) for b in buffers]
        ))
        """
        res = record_stream.read_array(period_size)
        record_buffer.put_samples(res)
        print "oh"
        time.sleep(0.1)
    
class Audio(object):

    def __init__(self, record_device, emit_device):
        self.record_device = record_device
        self.emit_device = emit_device
        self.record_stream = None
        self.emit_stream = None
        self.record_buffer = SampleBuffer(record_device.channels)
        self.emit_buffer = SampleBuffer(emit_device.channels)
        self.background_buffer = SampleBuffer(emit_device.channels)

    def start(self):
        self.emit_stream = Stream(self.emit_device, False, True)
        self.record_stream = Stream(self.record_device, True, True)
        self.emit_thread = threading.Thread(target=run_emit_thread,
            args=(self.emit_stream, [self.emit_buffer, self.background_buffer], self.record_stream, self.record_buffer))
        self.emit_thread.daemon = True
        self.emit_thread.start()

    """
    def io(self):
        if not self.record_stream:
            try:
                self.record_device.available(True)
                self.record_stream = Stream(self.record_device, True)
            except Exception as e:
                print "failed to init record_stream"
                traceback.print_exc()
                return False
        else:
            if not self.record_stream.assert_okay():
                self.record_stream.close()
                self.record_stream = None
                return False
        if not self.emit_stream:
            try:
                self.emit_device.available(False)
                self.emit_stream = Stream(self.emit_device, False, False)
            except Exception as e:
                print "failed to init emit_stream"
                traceback.print_exc()
                return False
        else:
            if not self.emit_stream.assert_okay():
                self.emit_stream.close()
                self.emit_stream = None
                return False
        return (self.record_stream, self.emit_stream)
    """

    def __enter__(self):
        return self.io()

    def __exit__(self, *rest):
        # Kludge o'clock
        try:
            self.record_stream.close()
            self.emit_stream.close()
        except:
            pass
        self.record_stream = None
        self.emit_stream = None
