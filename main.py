from tkinter import *
import vlc
import requests
from datetime import datetime
from mediaplayer import create_player, set_volume, get_track_info
from trackinfo import update_track_info

# Обновляем метку с временем
def update_time():
    current_time = datetime.now().strftime("%H:%M")
    time_label.config(text=f"Current local time: {current_time}")
    # Повторно запускаем эту функцию через 1 секунду
    root.after(1000, update_time)

def update_weather():
    # API key для доступа к погодному сервису (замените на свой собственный ключ)
    api_key = "40717ffd099e9b57a3dfdb38854180dd"  # Замените "your_api_key_here" на ваш API ключ
    # Запрос на получение погоды в Kharkiv
    url = f"http://api.openweathermap.org/data/2.5/weather?q=Kharkov&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    # Проверяем наличие ключей 'main' и 'weather' в полученных данных
    if 'main' in data and 'weather' in data:
        temperature = data['main']['temp']
        description = data['weather'][0]['description']
        # Обновляем метку с погодой
        weather_label.config(text=f"Weather in Kharkiv now: {temperature}°C, {description}")
    else:
        # Если ключи отсутствуют, выводим сообщение об ошибке
        weather_label.config(text="No weather data.")

    # Обновляем информацию о погоде и времени каждые 30 минут
    root.after(1800000, update_weather)

# Создаем экземпляр плеера с поддержкой метаданных
player = create_player()

def play_radio():
    selected_station_name = selected_station_var.get()
    if selected_station_name in radio_stations:
        selected_station_url = radio_stations[selected_station_name]
        media = vlc.Media(selected_station_url)
        player.set_media(media)
        player.play()
def stop_radio():
    player.stop()

def forward():
    global current_station_index
    current_station_index = (current_station_index + 1) % len(radio_stations)
    update_selected_station_label()
    play_radio()

def backward():
    global current_station_index
    current_station_index = (current_station_index - 1) % len(radio_stations)
    update_selected_station_label()
    play_radio()

def update_selected_station_label():
    selected_station_var.set(radio_station_names[current_station_index])

# Создаем главное окно
root = Tk()
root.title("OnAir International")
# Запрет изменения размеров окна
root.resizable(False, False)  # Первый аргумент - изменение размеров по горизонтали, второй - по вертикали
# Устанавливаем иконку для окна
root.iconbitmap(r"C:\Users\User\PycharmProjects\OnAir_Int\radio.ico")  # Замените "your_icon.ico" на путь к вашему файлу иконки
# Загружаем изображение
background_image = PhotoImage(file=r"C:\Users\User\PycharmProjects\OnAir_Int\background.png")
# Устанавливаем изображение в качестве фона окна
background_label = Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
# Устанавливаем фиксированный размер окна (ширина x высота)
root.geometry("600x140")

# Создаем экземпляр плеера
player = vlc.MediaPlayer()

# Добавляем элементы управления
volume_scale = Scale(root, from_=0, to=100, orient=HORIZONTAL)
volume_scale.set(50)  # Устанавливаем значение по умолчанию в середину
volume_scale.grid(row=1, column=0, padx=10, pady=10)  # Используем grid для добавления элемента на форму

# Метка для отображения информации о треке
track_info_label = Label(root, text="", wraplength=500)
track_info_label.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

# Функция для изменения громкости
def change_volume(value):
    player.audio_set_volume(int(value))

volume_scale.config(command=change_volume)

# Чтение ссылек на радиостанции из файла
radio_stations = {}
with open(r"C:\Users\User\PycharmProjects\OnAir_Int\radio_list.txt", "r", encoding='utf-8', errors='ignore') as file:
    for line in file:
        name, url = line.strip().split(": ")
        radio_stations[name] = url
        radio_station_names = list(radio_stations.keys())
        current_station_index = 0

# Добавляем элементы управления
selected_station_var = StringVar()
selected_station_var.set(radio_station_names[current_station_index])  # Устанавливаем текущую станцию по умолчанию

Label(root, text="Choose station:").grid(row=0, column=0)
stations_dropdown = OptionMenu(root, selected_station_var, *radio_stations.keys())
stations_dropdown.config(width=40)  # Задаем фиксированную ширину выпадающему меню
stations_dropdown.grid(row=0, column=1)

backward_button = Button(root, text="Backward", command=backward)
backward_button.grid(row=0, column=2)

play_button = Button(root, text="Play", command=play_radio)
play_button.grid(row=0, column=3)

stop_button = Button(root, text="Stop", command=stop_radio)
stop_button.grid(row=0, column=4)

forward_button = Button(root, text="Forward", command=forward)
forward_button.grid(row=0, column=5)

# Метка для отображения погоды
weather_label = Label(root, text="")
weather_label.grid(row=7, column=0, columnspan=4, sticky='w')

# Создаем метку для отображения времени
time_label = Label(root, text="")
time_label.grid(row=8, column=0, columnspan=4, sticky='w')

# Запускаем функцию обновления времени
update_time()

# Обновляем информацию о погоде
update_weather()

# Обновляем информацию о треке
update_track_info(root, player, track_info_label)

# Запускаем главный цикл событий
root.mainloop()
