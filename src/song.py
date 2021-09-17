from discord.player import FFmpegPCMAudio
from youtube_dl import YoutubeDL
import exceptions

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

class Song:
    def __init__(self, search_string):
        with YoutubeDL(YDL_OPTIONS) as ydl:
            try:
                song = ydl.extract_info("ytsearch:%s" % search_string, download=False)['entries'][0]
            except:
                raise exceptions.InvalidSongName(search_string)

        self._yt_url = f"https://www.youtube.com/watch?v={song['id']}"
        self._title = song["title"]
        self._audio_url = song["url"]
        self._duration = song["duration"]

    @property
    def description(self):
        hours = int(self._duration / 3600)
        minutes = int(self._duration / 60)
        seconds = self._duration % 60

        def padd(n):
            return f"0{n}" if n < 10 else str(n)

        return f"[{self._title}]({self._yt_url}) ({padd(hours)}:{padd(minutes)}:{padd(seconds)})"

    def audio(self):
        return FFmpegPCMAudio(self._audio_url, **FFMPEG_OPTIONS)