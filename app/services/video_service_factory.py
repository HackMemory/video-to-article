from services.video_service import VideoService
from services.youtube import YoutubeService

class VideoServiceFactory:
    @staticmethod
    def create_service(video_url: str) -> VideoService:
        if "youtube.com" in video_url:
            service = YoutubeService(video_url)
            service.is_youtube = True
            
            return service
        # Добавьте здесь условия для других сервисов, если необходимо
        else:
            raise ValueError("Unsupported video service")