import struct
import numpy as np

import math

from config import *

def pad_to_size(sample,length):
	zeroes = np.repeat(0,length - len(sample))
	return np.concatenate((sample,zeroes))

def open_wave(file):
	wf = wave.open(file,'rb')
	data = wf.readframes(CHUNK)
	while data != '':
		yield data
		data = wf.readframes(CHUNK)

def play_array(audio,data,rate_mutliplier=1,channels=None):
	data = pad_to_size(data,CHUNK * (1 + len(data) / CHUNK))
	frames = array_to_frames(data)
	play_frames(audio,frames,rate_mutliplier,channels=channels)

def play_frames(audio,frames,rate_mutliplier=1,channels=None):
	stream = audio.open(
		format=FORMAT,
		channels=channels or CHANNELS,
		rate=int(RATE * rate_mutliplier),
		frames_per_buffer=CHUNK,
		output_device_index=OUTPUT_DEVICE_INDEX,
		output=True
	)
	for f in frames:
		stream.write(f)
	stream.close()

def frames_to_file(frames,filename):
	file = open(filename,'w')
	for f in frames:
		file.write(f)
	file.close()

def chunks(l, n):
	for i in xrange(0, len(l), n):
		yield l[i:i+n]

def frames_to_array(frames):
	return np.transpose(np.reshape(
		np.fromstring(''.join(frames),dtype=NP_FORMAT),
		(CHUNK * len(frames),CHANNELS)
	))

def normalize(arr):
	if len(arr.shape) == 1:
		nx = np.empty((1,len(arr)))
		nx[0] = arr
		return nx
	return arr

def array_to_frames(arr):
	frames = []
	arr = normalize(arr)
	n_frames = int(math.ceil(float(arr.shape[1]) / CHUNK))
	pad_length = (n_frames * CHUNK) - arr.shape[1]
	pad_arr = np.zeros((arr.shape[0],pad_length))
	arr = np.append(arr,pad_arr,axis=1)
	arr = np.reshape(arr,(1,arr.shape[0] * arr.shape[1]),order='F')[0]
	res = list(arr)
	for chunk in chunks(res,CHUNK * CHANNELS):
		format = "%df" % (CHUNK * CHANNELS)
		frames.append(struct.pack(format,*chunk))
	return frames

	

	