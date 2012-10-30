from mplayer import Player as MPlayer
from threading import Timer

import time


class BasePlayer(object):
    def __init__(self, playEndedCallback):
        self.isPlaying = False
        self.mplayer = MPlayer(autospawn=False)

        self.timer = Timer(interval=1, function=Player.loop, args=[self])
        self.timer.start()

        self.playEndedCallback = playEndedCallback


    def stop(self):
        self.isPlaying = False
        self.mplayer.stop()


    def pause_resume(self):
        self.mplayer.pause()


    def seek(self, amount):
        if self.mplayer.time_pos:
            self.mplayer.time_pos += amount


    def play(self, mediafile):
        self.isPlaying = True
        args = []
        self.mplayer.args = args
        self.mplayer.spawn()
        if mediafile:
            self.mplayer.loadfile(mediafile)
        


    def quit(self):
        self.isPlaying = False
        self.timer.cancel()
        self.mplayer.quit()
        print "timer cancelled"


    @classmethod
    def loop(cls, player):

        #return if not playing
        if not player.isPlaying: return

        t = Timer(1, cls.loop, [player])
        t.start()

        # from videotop import status_bar
        # status_bar.set_text("%s/%s -- curr: %s" % ( player.player.length, player.player.time_pos, player.current))

        # print("%s/%s -- curr: %s" % ( player.mplayer.length, player.mplayer.time_pos, player.current))
        if player.mplayer.length != None:
            time.sleep(1000)
        else:
            player.playEndedCallback()
            t.cancel()

    def __del__(self):
        self.quit()


class PlayList(object):
    def __init__ (self):
        self.list = []
        self.currentIdx = 0
    
    def next(self):
        self.currentIdx += 1
        return self.current()


    def prev(self):
        self.currentIdx -= 1
        return self.current()


    def current (self):
        if self.currentIdx > len(self.list) - 1:
            self.currentIdx = 0
        elif self.currentIdx < 0:
            self.currentIdx = len(self.list) - 1
        return self.list[self.currentIdx]


    def append(self, mediafile):
        self.list.append(mediafile)


    def size(self):
        return len(self.list)


class Player(BasePlayer):
    def __init__(self):
        BasePlayer.__init__(self, self.__playEnded)
        self.playlist = PlayList()


    def play(self):
        BasePlayer.play(self, self.playlist.current())


    def next(self):
        BasePlayer.play(self, self.playlist.next())


    def prev(self):
        BasePlayer.play(self, self.playlist.prev())


    def getPlayList(self):
        return self.playlist


    def __playEnded(self):
        self.next()


player = Player()

if __name__ == '__main__':
    import os
    os.chdir("/home/boo/.videotop/videos")
    playlist = player.getPlayList()
    for f in os.listdir(".")[:2]:
        # player.addToPlayList(["-fs"], f)
        # player.addToPlayList([], f)
        playlist.append(f)
        #print "FILE", f
    from pprint import pprint
    pprint (player.playlist)
    player.play()
    from pdb import set_trace
    set_trace()
