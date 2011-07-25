# WARNING
This program is still under heavy development!

# DESCRIPTION
**Videotop** is a free console browser for online videos, written in python with vim-like keybindings.

# USAGE
If you are already familiar with vim the controls should be pretty intuitive.  
There are two modes: command mode and browse mode.

In command mode you can search for videos by typing **:s** *VIDEOSEARCH* and hitting **ENTER**.  
This will generate a list of videos and switch to browse mode.

In browse mode you can download the videos by hitting **ENTER** and play them with **p**.  
You can also open the youtube page by hitting **o**.  
**CTRL n** lists the next videos of your previous search and **CTRL r** clears the screen.

# COMMAND TABLE
<table border='1'>
<tr><th>Command Mode</th><th>Browse Mode</th><th>Description</th></tr>
<tr><td>:search, :s</td><td>s</td><td>Search for videos and switch to browse mode</td></tr>
<tr><td>:clear</td><td>CTRL r</td><td>Clear the video list and switch to command mode</td></tr>
<tr><td>:videos, :v</td><td></td><td>Show the downloaded videos and switch to browse mode</td></tr>
<tr><td>:13</td><td></td><td>Select video 13 and switch to browse mode</td></tr>
<tr><td></td><td>CTRL n</td><td>List the next videos of the previous search</td></tr>
<tr><td></td><td>ENTER</td><td>Download the selected video</td></tr>
<tr><td></td><td>o</td><td>Open the youtube site of the selected video in firefox</td></tr>
<tr><td></td><td>p</td><td>Play the selected video with mplayer</td></tr>
<tr><td></td><td>j</td><td>Move down</td></tr>
<tr><td></td><td>k</td><td>Move up</td></tr>
<tr><td></td><td>CTRL d</td><td>Move down</td></tr>
<tr><td></td><td>CTRL u</td><td>Move up</td></tr>
<tr><td></td><td>g</td><td>Move to the first video</td></tr>
<tr><td></td><td>G</td><td>Move to the last video</td></tr>
</table>

# DEPENDENCIES
* [urwid][1] to provide an ncurses frontend.
* [gdata][2] and [youtube-dl][3] to search for and download youtube videos.
* (optional) [mplayer][4] to play the downloaded videos.

[1]: http://excess.org/urwid/
[2]: http://code.google.com/apis/youtube/1.0/developers_guide_python.html
[3]: http://rg3.github.com/youtube-dl/
[4]: http://www.mplayerhq.hu/
