# from moviepy.editor import VideoFileClip
# clip = VideoFileClip("v.mp4")
# print( clip.duration )

# from pymediainfo import MediaInfo
# media_info = MediaInfo.parse('my_video_file.mov')
#duration in milliseconds
# duration_in_ms = media_info.tracks[0].duration


# import subprocess
# import re
 
# process = subprocess.Popen(['/usr/bin/ffmpeg',  '-i', "v.mp4"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
# stdout, stderr = process.communicate()
# matches = re.search(r"Duration:\s{1}(?P\d+?):(?P\d+?):(?P\d+\.\d+?),", stdout, re.DOTALL).groupdict()
 
# print matches['hours']
# print matches['minutes']
# print matches['seconds']



import moviepy.editor as mp
n="v.mp4"
duration =  mp.VideoFileClip("v.mp4").duration
print int(duration)