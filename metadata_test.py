import vlc
import time

# URL веб-радиостанции, которую вы хотите проверить
radio_url = "http://s17.myradiostream.com:10938/"

# Создаем экземпляр медиаплеера
instance = vlc.Instance('--no-video')
player = instance.media_player_new()

# Создаем медиа из URL веб-радиостанции
media = instance.media_new(radio_url)

# Добавляем медиа в медиаплеер
player.set_media(media)

# Воспроизводим веб-радиостанцию
player.play()

# Ожидаем некоторое время для получения метаданных
time.sleep(5)

# Получаем метаданные, если они доступны
meta = player.get_media().get_meta(vlc.Meta.NowPlaying)

# Выводим метаданные, если они были получены
if meta is not None:
    print("Метаданные:", meta)
else:
    print("Метаданные не доступны")

# Останавливаем воспроизведение
player.stop()
