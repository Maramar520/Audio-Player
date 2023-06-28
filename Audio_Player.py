import os
import threading
import time
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import themed_tk as tk
from mutagen.mp3 import MP3
from pygame import mixer

root = tk.ThemedTk()
root.get_themes()
root.set_theme("radiance")
root.config(bg='white')
root.resizable(0,0)

statusbar = ttk.Label(root, text="Welcome to My Audio Player",relief = SUNKEN, anchor=W, font='Times 10 italic')
statusbar.pack(side=BOTTOM, fill=X)

menubar = Menu(root)
root.config(menu=menubar)

subMenu = Menu(menubar, tearoff=0)

playlist = []


def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)

    mixer.music.queue(filename_path)


def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)

    playlist.insert(index, filename_path)
    index += 1


menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command=browse_file)
subMenu.add_command(label="Exit", command=root.destroy)


def about_us():
    tkinter.messagebox.showinfo('Audio Player','Audio Player menggunakan GUI Tkinter')


subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About Us", command=about_us)

mixer.init()

root.title("Audio Player")
root.iconbitmap(r'images/m.ico')

def del_song():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)

rightframe = Frame(root, bg='white')
rightframe.pack(pady=30)

def show_details(play_song):
    global total_length
    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    # div - total_length/60, mod - total_length % 60
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = "Total Length" + ' - ' + timeformat

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(t):
    global paused

    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat1 = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = "Current Time" + ' - ' + timeformat1
            a = current_time / float(total_length) * 100
            progress_bar["value"] = a
            time.sleep(1)
            current_time += 1


def play_music():
    global paused
    global play_it

    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('File not found', 'Melody could not find the file. Please check again.')

def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music Stopped"

paused = FALSE


def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music Paused"

def repeat_music():
    mixer.music.play(loops = -1)

def rewind_music():
    play_music()
    statusbar['text'] = "Music Rewinded"


def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)


muted = FALSE


def mute_music():
    global muted
    if muted:  # Unmute the music
        mixer.music.set_volume(1)
        volumeBtn.configure(image=volumePhoto)
        scale.set(100)
        muted = FALSE
    else:  # mute the music
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)
        scale.set(0)
        muted = TRUE

rightframe2 = Frame(rightframe, bg="white")
rightframe2.pack(side=LEFT)

addBtn = ttk.Button(rightframe2, text="+ Add", command=browse_file)
addBtn.pack(side=TOP, padx=20)

delBtn = ttk.Button(rightframe2, text="- Del", command=del_song)
delBtn.pack(side=TOP, padx=20)

topframe1= Frame(rightframe)
topframe1.pack()

namelist = ttk.Label(topframe1, text="Playlist", relief=GROOVE)
namelist.pack(fill=X)

playlistbox = Listbox(topframe1, width=40, height=15, relief=SUNKEN)
playlistbox.pack()

bottomframe = Frame(root, bg='white')
bottomframe.pack()

rewindPhoto = PhotoImage(file='images/rewind.png')
rewindBtn = Button(bottomframe, image=rewindPhoto, bg='white', command=rewind_music)
rewindBtn.grid(row=0, column=1, padx=2)

playPhoto = PhotoImage(file='images/play.png')
playBtn = Button(bottomframe, image=playPhoto, bg='white', command=play_music)
playBtn.grid(row=0, column=3, padx=2)

pausePhoto = PhotoImage(file='images/pause.png')
pauseBtn = Button(bottomframe, image=pausePhoto, bg='white', command=pause_music)
pauseBtn.grid(row=0, column=2, padx=2)

stopPhoto = PhotoImage(file='images/stop.png')
stopBtn = Button(bottomframe, image=stopPhoto, bg='white', command=stop_music)
stopBtn.grid(row=0, column=4, padx=2)

mutePhoto = PhotoImage(file='images/mute.png')
volumePhoto = PhotoImage(file='images/volume.png')
volumeBtn = Button(bottomframe, image=volumePhoto, bg='white', command=mute_music)
volumeBtn.grid(row=0, column=6, padx=2)

scale = ttk.Scale(bottomframe, from_=100, to=0, orient=VERTICAL, command=set_vol)
scale.set(100)
mixer.music.set_volume(1)
scale.grid(row=0, column=7, padx=2)

topframe = Frame(root, bg='white')
topframe.pack()

currenttimelabel = ttk.Label(topframe, text='Current Time - --:--')
currenttimelabel.grid(row=0, column=0)

lengthlabel = ttk.Label(topframe, text='Total Length - --:--')
lengthlabel.grid(row=0, column=1)

progress_bar = ttk.Progressbar(root, orient='horizontal', mode='determinate', length=600)
progress_bar.pack()

def on_closing():
    stop_music()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()