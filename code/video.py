from contextlib import closing
from videosequence import VideoSequence   






with closing(VideoSequence("v.mp4")) as frames:
	for idx, frame in enumerate(frames[:100]):
		s="img/"
		frame.save(s+"1_{:02d}.jpg".format(idx+1))