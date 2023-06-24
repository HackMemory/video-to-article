import os
from dotenv import load_dotenv
from pathlib import Path

class Config:
    def __init__(self):
        load_dotenv()  # Загрузка переменных окружения из файла .env

        self.video_storage_path = os.getenv("VIDEO_STORAGE_PATH")
        self.picture_storage_path = os.getenv("PICTURE_STORAGE_PATH")
        self.temp_folder_path = os.getenv("TEMP_FOLDER_PATH")
        self.max_concurrent_jobs = int(os.getenv("MAX_CONCURRENT_JOBS"))
        self.whisper_model_name = os.getenv("WHISPER_MODEL_NAME")


        Path(self.video_storage_path).mkdir(parents=True, exist_ok=True)
        Path(self.picture_storage_path).mkdir(parents=True, exist_ok=True)
        Path(self.temp_folder_path).mkdir(parents=True, exist_ok=True)

config = Config()

