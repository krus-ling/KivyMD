import requests

# URL для отправки запроса
url = 'http://127.0.0.1:8000/get_transcription'

# Открытие файла для отправки
with open('myrecording.wav', 'rb') as file:
    files = {'file': file}

    # Отправка POST-запроса с файлом
    resp = requests.post(url=url, files=files)

# Вывод ответа от сервера
print(resp.json())
