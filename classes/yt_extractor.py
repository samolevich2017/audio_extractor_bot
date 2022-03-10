from numpy import empty
from pytube import YouTube
import os
import re
import utils.extfunctions as utils

# Class for processing videos from YouTube
class YT_Extractor:

    # basic constructor
    def __init__(self, url):
        self.yt = YouTube(str(url))

    # get title current track
    def get_track_title(self):
        return self.yt.title

    # get duration of current track
    def get_duration(self):
        return self.yt.length

    # function for extract audio from video by url
    def extract(self):

        # extract only audio
        video = self.yt.streams.filter(only_audio=True).first()

        # destination is directory "music"
        destination = "music/"

        # download the file
        out_file = video.download(output_path=destination)

        # save the file
        base, ext = os.path.splitext(out_file)
        new_file = str(re.sub(r"[#@*''$.%|~,&!?«»¥¤¨©´°¿º►]", "", base)).replace('"',"") + '.mp3'
        new_file = utils.deEmojify(new_file)
        print("New file => ?", new_file)
        print("Out file => ?", out_file)
        os.rename(out_file, new_file)

        # result of success
        print(self.yt.title + " has been successfully downloaded.")

        # path to audio file
        title_audio = str(re.sub(r"[#@*''$.%/|~,&!?:«»¥¤¨©´°¿º►]", "", self.yt.title)).replace('"',"")
        title_audio = utils.deEmojify(title_audio)
        
        return f"{destination}{title_audio}.mp3"

