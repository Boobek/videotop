from mplayer import Player as MPlayer
from threading import Timer

import time


class Player(object):
    def __init__(self):
        self.isPlaying = False
        self.player = MPlayer(autospawn=False)
        self.playlist = []
        self.current = 0

        self.timer = Timer(interval=1, function=Player.loop, args=[self])
        #self.thread.daemon = True
        self.timer.start()


    def play(self):
        self.isPlaying = True
        self.__play()


    def stop(self):
        self.isPlaying = False
        self.player.stop()


    def pause_resume(self):
        self.player.pause()


    def seek(self, amount):
        if self.player.time_pos:
            self.player.time_pos += amount


    def __play(self):
        if len(self.playlist) > self.current:
            args = self.playlist[self.current][0]
            mediafile = self.playlist[self.current][1]
            self.player.args = args
            self.player.spawn()
            if mediafile:
                self.player.loadfile(mediafile)


    def playNext(self):
        if len(self.playlist) > self.current:
            self.current += 1
            self.play()


    @classmethod
    def loop(cls, player):
        t = Timer(1, cls.loop, [player])
        t.start()

        if not player.isPlaying: return

        from videotop import status_bar
        status_bar.set_text("%s/%s -- curr: %s" % ( player.player.length, player.player.time_pos, player.current))

        if player.player.length != None and player.current < len(player.playlist):
            time.sleep(1000)
            print player.player.length
        else:
            player.playNext()


    def addToPlayList(self, args, mediafile=None):
        self.playlist.append( [args, mediafile])


    def __del__(self):
        self.timer.cancel()
        self.player.quit()

player = Player()

if __name__ == '__main__':
    import os
    os.chdir("/home/boo/.videotop/videos")
    for f in os.listdir(".")[:2]:
        player.addToPlayList(["-fs"], f)
        #print "FILE", f
    from pprint import pprint
    pprint (player.playlist)
    player.play()