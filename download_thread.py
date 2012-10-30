import threading
import subprocess
from subprocess import Popen, PIPE


class DownloadThread(threading.Thread):

    def __init__(self, title, url):
        threading.Thread.__init__(self)
        self.progress = 'Preparing download...'
        self.updated = True
        self.killed = False

        # create the youtube-dl subprocess
        file = title + '.%(ext)s'
        output = '--output=' + file
        max_quality = '--max-quality=35'
        command = ['youtube-dl', '--no-part', '--continue', max_quality, output, url]
        self.download_process = Popen(command, stdout=PIPE, universal_newlines=True)

    def kill(self):
        self.download_process.kill()
        self.killed = True

    def run(self):
        while self.progress != '':
            self.progress = self.download_process.stdout.readline()
            self.updated = True
        if self.killed:
            self.progress = 'Aborted downloading'
        else:
            self.progress = 'Finished downloading'

class StreamThread(threading.Thread):

    def __init__(self, video, displayVideo=False):
        threading.Thread.__init__(self)
        self.progress = 'Preparing download...'
        self.updated = True
        self.killed = False

        self.video = video
        self.displayVideo = displayVideo

    def kill(self):
        self.download_process.kill()
        self.killed = True

    def run(self):
        cookie = '/tmp/videotop_cookie'
        cmd1 = ['youtube-dl', '--get-url', '--max-quality=34', '--cookies=' + cookie, self.video.url]
        cmd2 = ['mplayer', '-prefer-ipv4', '-msgcolor', '-title', self.video.title]

        stream = subprocess.check_output(cmd1).strip()

            # if not self.displayVideo:
            #     cmd2.append("-novideo")
        cmd2.extend(['-cookies', '-cookies-file', cookie, stream])
        from subprocess import PIPE
        subprocess.call(cmd2)
