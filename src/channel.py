import json
import os

from googleapiclient.discovery import build


class YoutubeMixin:
    @classmethod
    def get_service(cls):
        # создать специальный объект для работы с API
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube


class Channel(YoutubeMixin):
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self._channel_id = channel_id
        self.__channel_id = channel_id
        self.channel = self.get_service().channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title = self.channel["items"][0]["snippet"]["title"]
        self.description = self.channel["items"][0]["snippet"]["description"]
        self.customUrl = f"https://www.youtube.com/channel/{self.__channel_id}"
        self.viewCount = self.channel["items"][0]["statistics"]["viewCount"]
        self.subscriberCount = int(self.channel["items"][0]["statistics"]["subscriberCount"])
        self.videoCount = self.channel["items"][0]["statistics"]["videoCount"]

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=4, ensure_ascii=False))

    @property
    def channel_id(self):
        return self.__channel_id

    def to_json(self, f):
        task1 = {
            'id': self.__channel_id,
            'title': self.title,
            'description': self.description,
            'view_count': self.viewCount,
            'subscriber_count': self.subscriberCount,
            'video_count': self.videoCount,
            'url': self.customUrl
        }
        with open(f, 'w', encoding='utf-8') as file:
            json.dump(task1, file, indent=2, ensure_ascii=False)

    @channel_id.setter
    def channel_id(self, value):
        self._channel_id = value
