from stream import create_stream, SampleBuffer

def playback(stream, queue):
	while True:
		stream.write(queue.get())

class Emitter(object):
	def __init__(self, settings):
		self.buffer = SampleBuffer(channels=settings.output.channels)
		self.stream = create_stream(
			settings=settings,
			output=True,
			callback=lambda *args: self.playback(*args)
		)

	def playback(self, output, *rest):
		output[:] = self.buffer.get_samples(len(output))

	def emit(self, arr):
		self.buffer.put(arr)

	def start(self):
		self.stream.start()

	def stop(self):
		self.stream.stop()

	def rate(self):
		return int(self.stream.samplerate)