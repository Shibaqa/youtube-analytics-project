import os
from datetime import timedelta
import isodate
from googleapiclient.discovery import build


class PlayList:
    def __init__(self, playlist_id, title=None, url=None,
                 youtube=build('youtube', 'v3', developerKey=os.getenv('YT_API_KEY'))):

        self.playlist_id = playlist_id
        self.url = url
        self.youtube = youtube
        self.playlist_videos = self.youtube.playlistItems().list(playlistId=playlist_id,
                                                                 part='contentDetails, snippet',
                                                                 maxResults=50,
                                                                 ).execute()
        self.channel_id = self.playlist_videos['items'][0]['snippet']['channelId']
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                         id=','.join(self.video_ids)
                                                         ).execute()
        self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']
        self.playlists = self.youtube.playlists().list(channelId=self.channel_id,
                                                       part='contentDetails,snippet',
                                                       maxResults=50,
                                                       ).execute()
        for video in self.playlists['items']:
            if video['id'] == self.playlist_id:
                # print(self.playlist_id)
                self.title = video['snippet']['title']
            # print(self.title)

    @property
    def total_duration(self):
        sum = timedelta(hours=0, minutes=0, seconds=0)
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            sum += duration
        return sum

    # @property
    def show_best_video(self):
        max_like = 0
        url_top = ""
        for likes in self.video_response['items']:
            like = int(likes['statistics']['likeCount'])
            if max_like <= like:
                max_like = like
                url_top = f"https://youtu.be/{likes['id']}"
        return url_top
