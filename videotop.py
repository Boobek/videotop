#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os
import urwid
import youtube_client

class VideoButton(urwid.FlowWidget):
    def __init__(self, video, index, color='index'):
        self.video = video
        self.index = index
        index = urwid.Text((color, str(self.index)))
        try:
            rounded_rating = str(round(float(self.video.rating), 1))
        except:
            rounded_rating = self.video.rating

        width = 30
        duration = self.video.formatted_duration()
        views = urwid.Text([(color, 'Views: '), self.video.views])
        rating = urwid.Text([(color, 'Rating: '), rounded_rating])
        author = urwid.Text([(color, 'Author: '), self.video.author])
        duration = urwid.Text([(color, 'Duration: '), duration, '\n'])
        button_info = urwid.Columns([('fixed', width, author), ('fixed', width, views),
                                     ('fixed', width, rating), ('fixed', width, duration)])
        title = urwid.Text(self.video.title)
        button = urwid.Pile([title, button_info])

        index_width = int(len(str(self.index)) + 2)
        if index_width == 3:
            index_width += 1 # align the first 9 videos
        self.display_widget = urwid.Columns([('fixed', index_width, index), button])
        self.display_widget = urwid.AttrMap(self.display_widget, None, 'focus')
    def rows(self, size, focus=False):
        return self.display_widget.rows(size, focus)
    def render(self, size, focus=False):
        return self.display_widget.render(size, focus)
    def selectable(self):
        return True
    def keypress(self, size, key):
        if key == 'enter':
            self.display_widget.set_attr_map({None: 'downloaded'})
            status_bar.set_text('Downloading: ' + self.video.title)
            self.video.download()
        elif key == 'o':
            self.display_widget.set_attr_map({None: 'opened'})
            #self.button.set_focus_map({None: 'opened'})
            status_bar.set_text('Opening in browser: ' + self.video.title)
            self.video.open()
        elif key == 'p':
            status_bar.set_text('Playing: ' + self.video.title)
            self.video.play()
        elif key == 'a':
            status_bar.set_text(self.video.abort())
        else:
            return key

class CommandPrompt(urwid.Edit):
    def clear(self):
        self.set_caption('')
        self.set_edit_text('')
    def keypress(self, size, key):
        if key == 'enter' and not self.get_edit_text() == '':
            if self.caption == '/':
                pattern = self.get_edit_text()
                self.clear()
                listbox.search(pattern)
                return
            command = self.get_edit_text()
            command = command.split(' ', 1)
            if command[0] in ('search', 's'):
                query = command[1]
                self.clear()
                status_bar.set_text('Searching for: ' + query)
                loop.draw_screen()
                search = client.search(query) # takes the most time
                listbox.append(search)
                status_bar.set_text(query)
                main_frame.set_focus('body')
            elif command[0] in ('search_user', 'su'):
                user = command[1]
                self.clear()
                status_bar.set_text('Searching for videos by: ' + user)
                loop.draw_screen()
                search = client.search_user(user) # takes the most time
                listbox.append(search)
                status_bar.set_text(user)
                main_frame.set_focus('body')
            elif command[0] == 'related':
                self.clear()
                status_bar.set_text('Searching for related videos...')
                loop.draw_screen()
                # current_video_id should be in youtube_client.YouTubeVideo
                current_video_id = listbox.get_focus().video.entry.id.text.split('/')[-1]
                related_videos = client.get_related_videos(current_video_id) # takes the most time
                listbox.append(related_videos)
                main_frame.set_focus('body')
            elif command[0] in ('videos', 'v'):
                self.clear()
                status_bar.set_text('Listing local videos')
                loop.draw_screen()
                video_list = os.listdir(os.getcwd())
                video_list = [os.path.splitext(video)[0] for video in video_list]
                video_list.sort()
                videos = [client.get_local_video(video) for video in video_list]
                listbox.append(videos, color='local_video')
                main_frame.set_focus('body')
            elif command[0] == 'clear':
                listbox.clear()
                self.set_edit_text('')
            elif command[0].isdigit():
                self.clear()
                video_focus = int(command[0]) - 1
                listbox.set_focus(video_focus)
                main_frame.set_focus('body')
            elif command[0] in ('quit', 'q'):
                raise urwid.ExitMainLoop()
            else:
                status_bar.set_text('Error, there is no command named "' + command[0] + '"')
                pass
        if key in ('esc', 'ctrl x'):
            main_frame.set_focus('body')
            self.clear()
        else:
            return urwid.Edit.keypress(self, size, key)

class VideoListBox(urwid.WidgetWrap):
    def __init__(self):
        self.latest_search = None
        self.latest_search_position = None
        self.body = urwid.SimpleListWalker([])
        self.listbox = urwid.ListBox(self.body)
        urwid.WidgetWrap.__init__(self, self.listbox)
    def append(self, search, color='index'):
        for video in search:
            new_button = VideoButton(video, int(len(self.body)) + 1, color)
            self.body.append(new_button)
            loop.draw_screen()
    def clear(self):
        status_bar.set_text('Cleared the screen.')
        self.body[:] = []
    def set_focus(self, position):
        self.listbox.set_focus(position)
    def get_focus(self):
        return self.listbox.get_focus()[0]
    def search(self, pattern):
        video_list = [video_button.video.title for video_button in self.body]
        index_list = []
        for video in video_list:
            if pattern in video:
                index_list.append(video_list.index(video))
        self.latest_search = index_list
        self.latest_search_position = 0
        try:
            first_result = self.latest_search[self.latest_search_position]
            self.set_focus(first_result)
        except:
            status_bar.set_text('Error, could not find pattern "' + pattern + '"')
        main_frame.set_focus('body')
    def keypress(self, size, key):
        if key == ':':
            main_frame.set_focus('footer')
            command_prompt.set_caption(':')
        if key == '/':
            main_frame.set_focus('footer')
            command_prompt.set_caption('/')
        elif key == 'j':
            self.listbox.keypress(size, 'down')
        elif key == 'k':
            self.listbox.keypress(size, 'up')
        elif key == 'g':
            self.listbox.change_focus(size, 0)
        elif key == 'G':
            self.listbox.change_focus(size, len(self.body) - 1)
        elif key == 'ctrl d':
            position = self.listbox.get_focus()[1] + 5
            self.listbox.set_focus(position, 'above')
        elif key == 'ctrl u':
            position = self.listbox.get_focus()[1] - 5
            if position < 0:
                position = 0
            self.listbox.set_focus(position, 'below')
        elif key == 'ctrl r':
            self.clear()
        elif key == 'ctrl n':
            search = client.next_page()
            self.append(search)
        elif key == 'n':
            try:
                self.latest_search_position += 1
                self.listbox.set_focus(self.latest_search[self.latest_search_position])
            except:
                self.latest_search_position = 0
                self.listbox.set_focus(self.latest_search[self.latest_search_position])
        elif key == 'N':
            try:
                self.latest_search_position -= 1
                self.listbox.set_focus(self.latest_search[self.latest_search_position])
            except:
                self.latest_search_position = len(self.latest_search) - 1
                self.listbox.set_focus(self.latest_search[self.latest_search_position])
        else:
            return self.listbox.keypress(size, key)

# change to download directory
home_dir = os.environ['HOME']
download_dir = os.path.join(home_dir, '.videotop')
os.chdir(download_dir)

palette = [('focus', 'light red', 'black', 'standout'),
          ('status', 'white', 'dark blue'),
          ('opened', 'light blue', 'black'),
          ('downloaded', 'white', 'black'),
          ('local_video', 'yellow', 'black'),
          ('index', 'dark cyan', 'black')]
listbox = VideoListBox()
command_prompt = CommandPrompt('')
status_bar = urwid.Text('Press enter to search', align='left')
footer = urwid.Pile([urwid.AttrMap(status_bar, 'status'), command_prompt])
main_frame = urwid.Frame(listbox)
main_frame.set_footer(footer)
client = youtube_client.YouTubeClient()

def handle_input(input):
    pass

loop = urwid.MainLoop(main_frame, palette, unhandled_input=handle_input)
loop.run()
