from pytube import YouTube
import yt_dlp as youtube_dl
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
        path = video.download(output_path=config.video_storage_path, filename=video_file)
        return path

    def get_episodes(self):
        # Опции извлечения метаданных
        ydl_opts = {
            'skip_download': True,  # Пропустить загрузку видео
            'writeinfojson': True,  # Сохранить метаданные в JSON файл
        }

        # Создание объекта YouTubeDL и извлечение метаданных видео
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            data = []
            info = ydl.extract_info(self.video_url, download=False)

            # Получение списка эпизодов из метаданных
            episodes = info.get('chapters', [])

            # Вывод списка эпизодов, их таймкодов и названий
            for i, episode in enumerate(episodes):
                start_time = episode.get('start_time')
                end_time = episode.get('end_time')
                title = episode.get('title')
                data.append({"title": title, "start_time": start_time, "end_time": end_time})

            return data