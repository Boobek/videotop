import gdata.youtube
import gdata.youtube.service
import webbrowser
import subprocess
import locale
import download_thread
import os
import logging

from pyqutie.config import SavedConfig
cfg = SavedConfig("youtube");

log = logging.getLogger("base.ytservice");

locale.setlocale(locale.LC_ALL, '')
from player import player

class YouTubeClient:
    def __init__(self):
        self.yt_service = gdata.youtube.service.YouTubeService()
        self.max_results = 25
        self.last_search = None

        self.yt_service.developer_key = "AI39si7HTYNNRVgmteKq-kMGDfCFPrSJfMCux4zK39n_TocNSpyYPYclMv7NCzy8aIeLu1Q5cS_sh9i8iw6NZbCWip2GaElBWw"
        self.yt_service.client_id = 'youtubeplayer'
        self.yt_service.ssl = True


    def search(self, search_terms, page=1):
        self.last_search = [search_terms, page]
        query = gdata.youtube.service.YouTubeVideoQuery()
        query.vq = search_terms
        # query.start_index is 1 based
        query.start_index = (page - 1) * int(self.max_results) + 1
        query.max_results = self.max_results
        try:
            feed = self.yt_service.YouTubeQuery(query)
            return self.get_videos(feed)
        except gdata.service.RequestError:
            return []

    def get_videos(self, feed):
        videos = []
        for entry in feed.entry:
            new_video = YouTubeVideo(entry)
            videos.append(new_video)
        return videos

    def next_page(self):
        return self.search(self.last_search[0], self.last_search[1] + 1)

    def get_local_video(self, video_title):
        # replace html code &#47; with slashes
        video_title = video_title.replace('&#47;', '/')
        title = gdata.media.Title(text=video_title)
        group = gdata.media.Group(title=title)
        video_entry = gdata.youtube.YouTubeVideoEntry(media=group)
        return YouTubeVideo(video_entry)


    def login(self, email=None, pwd=None):
        if email is not None and pwd is not None:
            cfg.email = email
            cfg.pwd = pwd
        else:
            try:
                email = cfg.email
                pwd = cfg.pwd
            except:
                return
        self.yt_service.email = email
        self.yt_service.password = pwd
        self.yt_service.source = 'youtubeplayer'
        self.yt_service.ProgrammaticLogin()


    def getUserPlayLists(self):
        _pls = self.yt_service.GetYouTubePlaylistFeed()
        pls = []
        for entry in _pls.entry:
            pl = YoutubePlayList(entry)
            pls.append(pl)
        return pls


class YouTubeVideo:
    downloads = []

    def __init__(self, entry):
        self.entry = entry
        self.title = entry.media.title.text
        self.download_process = None
        self.player = player
        # replace slashes with html code &#47;
        self.filename = self.title.replace('/', '&#47;')

        try:
            self.url = entry.media.player.url
            self.description = entry.media.description.text
            self.author = entry.author[0].name.text
            self.published = entry.published.text.split('T')[0]
        except:
            # dunno, local video
            self.author = 'N/A'
            self.published = 'N/A'

        try:
            self.duration = entry.media.duration.seconds
            self.duration = self.get_formatted_duration()
        except AttributeError:
            self.duration = 'N/A'

        try:
            self.views = entry.statistics.view_count
            self.views = self.get_formatted_views()
        except AttributeError:
            self.views = 'N/A'

        try:
            self.rating = entry.rating.average
            self.rating = str(round(float(self.rating), 1))
        except AttributeError:
            self.rating = 'N/A'

    def open(self):
        webbrowser.open_new_tab(self.url)

    def download(self):
        self.dl = download_thread.DownloadThread(self.filename, self.url)
        self.dl.start()
        YouTubeVideo.downloads.append(self)

    def abort(self):
        try:
            self.dl.kill()
            return 'Aborted downloading "' + self.title + '"'
        except:
            return 'Aborting downloading "' + self.title + '" failed'

    def get_formatted_duration(self):
        m, s = divmod(int(self.duration), 60)
        h, m = divmod(m, 60)
        formatted_duration = "%d:%02d:%02d" % (h, m, s)
        return formatted_duration

    def get_formatted_views(self):
        return locale.format('%d', int(self.views), grouping=True)

    def play(self, displayVideo=False):
        extensions = ['.flv', '.mp4', '.webm']
        for ext in extensions:
            file = self.filename + ext
            if os.path.exists(file):
                ex = ['-use-filename-title']
                if not displayVideo:
                    ex.append('-novideo')

                player.addToPlayList(ex, file)
                #self.player.args = ex
                #self.player.spawn()
                #self.player.loadfile(file)
                return True
        return False

    def stream(self, displayVideo=False):
        self.pl = download_thread.StreamThread(self, displayVideo)
        self.pl.start()


class YoutubePlayList(object):
    def __init__(self, entry):
        self.entry = entry
        log.info("Loading playlist %s" , entry.title.text)
        self._playlist = None


    def __getFullPlayList(self):
        if self._playlist is None:
            self._playlist = ytclient.yt_service.GetYouTubeVideoFeed(self.entry.feed_link[0].href)


    def title(self):
        return self.entry.title.text


    def getVideos(self):
        self.__getFullPlayList()
        videos = []
        for entry in self._playlist.entry:
            videos.append(YouTubeVideo(entry))
        return videos
        


ytclient = YouTubeClient()
# ytclient.login("boobeksp@gmail.com", "a123456")
# pls = ytclient.getUserPlayLists()
# vids = pls[0].getVideos()
# import pdb
# pdb.set_trace()