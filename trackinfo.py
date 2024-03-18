# trackinfo.py
from tkinter import *

def update_track_info(root, player, label):
    track_info = get_track_info(player)
    label.config(text="Now playing: " + track_info)
    root.after(1000, update_track_info, root, player, label)

def get_track_info(player):
    # Этот метод будет взят из mediaplayer.py
    return "Unknown"
