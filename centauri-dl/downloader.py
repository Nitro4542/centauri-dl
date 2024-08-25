import requests
import yt_dlp

class Downloader:
    def __init__(self, url, download_format, output_folder, yt_dlp_options=None):
        self.url = url
        self.output_folder = str(output_folder)
        self.format = int(download_format)

        if yt_dlp_options:
            self.yt_dlp_options = yt_dlp_options
            self.yt_dlp_options_backup = yt_dlp_options
        else:
            self.yt_dlp_options = {"format":"best", "outtmpl":"%(title)s.%(ext)s"}
            self.yt_dlp_options_backup = {"format": "best", "outtmpl": self.output_folder + "/%(title)s.%(ext)s"}

    def download(self):
        if self.format == 1:
            self.yt_dlp_options.update(self.yt_dlp_options_backup)
            with yt_dlp.YoutubeDL(self.yt_dlp_options) as ydl:
                ydl.download([self.url])
        else:
            self.yt_dlp_options.update({"format":"m4a/bestaudio/best", "postprocessors": [{"key":"FFmpegExtractAudio", "preferredcodec": "m4a"}]})
            with yt_dlp.YoutubeDL(self.yt_dlp_options) as ydl:
                ydl.download([self.url])

    def check_url(self):
        if self.url.startswith("https://youtube.com/watch?v=") or self.url.startswith("https://youtube.com"):
            response = requests.get(self.url)
            if response.status_code == 200:
                return 0
            else:
                return response.status_code
        else:
            return 1