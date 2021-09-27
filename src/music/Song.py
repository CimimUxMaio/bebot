import lyricsgenius as lg
from discord.player import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from config import GENIUS_ACCESS_TOKEN
import exceptions
import re


YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

LyricsGenius = lg.Genius(GENIUS_ACCESS_TOKEN)
LyricsGenius.verbose = False
LyricsGenius.remove_section_headers = True
LyricsGenius.skip_non_songs = True


class Song:
    def __init__(self, ctx, search):
        self.ctx = ctx
        with YoutubeDL(YDL_OPTIONS) as ydl:
            try:
                song = ydl.extract_info("ytsearch:%s" % search, download=False)['entries'][0]
            except:
                raise exceptions.InvalidSongName(search)

        self._yt_url = f"https://www.youtube.com/watch?v={song['id']}"
        self._title = song["title"]
        self._audio_url = song["url"]
        self._duration = song["duration"]
        self._lyrics_searched = False
        self._lyrics = None

    @property
    def description(self):
        hours, remainder = divmod(self._duration, 3600)
        minutes, remainder = divmod(remainder, 60)
        seconds = remainder % 60

        def pad(n):
            return f"0{n}" if n < 10 else str(n)

        return f"[{self._title}]({self._yt_url}) ({pad(hours)}:{pad(minutes)}:{pad(seconds)})"


    @property
    def title(self):
        return self._title

    @property
    def lyrics(self):
        if not self._lyrics_searched:
            self._lyrics = self._request_lyrics()

        return self._lyrics

    def audio(self):
        return FFmpegPCMAudio(self._audio_url, **FFMPEG_OPTIONS)

    def _request_lyrics(self):
        unwanted_re = "(\(.*?\))|(\[.*?\])"
        formatted_title = re.sub(unwanted_re, "", self.title).strip()
        res = LyricsGenius.search_song(formatted_title, get_full_info=False)
        self._lyrics_searched = True
        return res.lyrics if res else None