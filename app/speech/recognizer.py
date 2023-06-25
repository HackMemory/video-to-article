import whisper
from config import config

def format_item(item):
    return {
        "time": item["start"],
        "text": item["text"]
    }

class Recognizer:
    model = None

    def __init__(self):
        self.model = whisper.load_model(config.whisper_model_name, download_root=config.temp_folder_path)

    def transcribe(self, path):
        result = self.model.transcribe(path)

        segments = []
        for item in result["segments"]:
            segments.append(format_item(item))

        data = {
            "text": result['text'],
            "segments": segments
        }

        return data

recognizer = Recognizer()
