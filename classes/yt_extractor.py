from pytube import YouTube
import os
import re
import utils.extfunctions as utils

# Class for processing videos from YouTube
class YT_Extractor:

    # function for extract audio from video by url
    def extract(self, url):
        
        # url input from user
        yt = YouTube(str(url))

        # extract only audio
        video = yt.streams.filter(only_audio=True).first()

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
        print(yt.title + " has been successfully downloaded.")

        # path to audio file
        title_audio = str(re.sub(r"[#@*''$.%/|~,&!?:«»¥¤¨©´°¿º►]", "", yt.title)).replace('"',"")
        title_audio = utils.deEmojify(title_audio)
        
        return f"{destination}{title_audio}.mp3"

        