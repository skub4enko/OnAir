# mediaplayer.py
import vlc
import time

def create_player():
    # Инициализация экземпляра медиаплеера
    instance = vlc.Instance()
    # Устанавливаем уровень логирования для включения метаданных
    instance.set_log_verbosity(2)
    player = instance.media_player_new()
    return player
def set_volume(player, volume):
    player.audio_set_volume(int(volume))

# Ожидаем некоторое время для получения метаданных
    time.sleep(10)
def get_track_info(player):
    media = player.get_media()
    if media is not None:
        meta = media.get_meta(vlc.Meta.NowPlaying)
        if meta is not None:
            return meta
    return "Unknown"
