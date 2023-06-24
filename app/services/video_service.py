import abc

class VideoService(abc.ABC):
    is_youtube = False

    @abc.abstractmethod
    def download_video(self) -> str:
        pass