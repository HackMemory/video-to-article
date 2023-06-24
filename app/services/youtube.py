from pytube import YouTube
from services.video_service import VideoService
from config import config
import hashlib
from pathlib import Path
import os

class YoutubeService(VideoService):

    video_url = ''

    def __init__(self, video_url) -> None:
        self.video_url = video_url

    def download_video(self) -> str:
        yt = YouTube(self.video_url)

        hash_file = hashlib.md5()
        hash_file.update(yt.title.encode())

        video = yt.streams.get_highest_resolution()
        video_file = f'{hash_file.hexdigest()}.mp4'
        res = video.download(output_path=config.video_storage_path, filename=video_file)
        return res