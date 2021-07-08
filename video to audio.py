from moviepy.editor import *


def vid_to_aud(vid, aud='audio.wav'):
    video = VideoFileClip(vid)
    audio = video.audio
    audio.write_audiofile(aud)


vid_to_aud('video.mkv')
