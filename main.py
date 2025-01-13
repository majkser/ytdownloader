import tkinter as tk
from tkinter import messagebox
import yt_dlp

type = input("Do you want to download a video or audio? (enter 'video' or 'audio'): " )
url = input(f"Enter the URL of the {type} you want to download: ")

vid_opts = {
    'format': "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4] / bv*+ba/b",
    'outtmpl': '%(title)s.%(ext)s',
}

sound_opts = {
    'format': 'ba[ext=m4a]',
    'outtmpl': '%(title)s.%(ext)s',
}

if type == 'video':
    ydl_opts = vid_opts
elif type == 'audio':
    ydl_opts = sound_opts

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])