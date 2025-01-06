"""
Тест записи с микрофона для ПК!
"""

import os
import pyaudio
import wave
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDRoundFlatButton
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from threading import Event


class AudioRecorder:
    def __init__(self):
        self.audio = None
        self.frames = []
        self.stream = None
        self.file_path = "myrecording.wav"
        self.audio_gate = Event()  # Синхронизация доступа
        self.audio_gate.set()  # Разрешаем доступ сразу

    def reset_audio(self):
        """Останавливает старые соединения и очищает данные перед началом новой записи."""
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()

        if self.audio is not None:
            self.audio.terminate()

        # Очищаем старые данные
        self.frames = []
        self.audio = pyaudio.PyAudio()

        # Удаляем старый файл записи, если он существует
        if os.path.exists(self.file_path):
            try:
                os.remove(self.file_path)
                print(f"Удален старый файл: {self.file_path}")
            except Exception as e:
                print(f"Не удалось удалить файл: {e}")

    def start_recording(self):
        """Начинает запись с нуля, сбрасывая все старые данные и соединения"""
        self.reset_audio()  # Сброс старых данных и потоков

        self.audio_gate.wait()  # Блокируем доступ, если запись/воспроизведение идет
        self.audio_gate.clear()  # Блокируем другие потоки

        try:
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                frames_per_buffer=1024
            )
            # Планируем чтение аудио
            Clock.schedule_interval(self.record_chunk, 0)  # 0 - записываем бесконечно
            print("Запись началась.")
        except IOError as e:
            print(f"Ошибка при открытии потока: {e}")

    def stop_recording(self):
        """Останавливает запись и сохраняет файл"""
        Clock.unschedule(self.record_chunk)  # Прекращаем запись

        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()

        self.audio.terminate()

        # Сохраняем аудиофайл
        try:
            sound_file = wave.open(self.file_path, "wb")
            sound_file.setnchannels(1)
            sound_file.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            sound_file.setframerate(44100)
            sound_file.writeframes(b''.join(self.frames))
            sound_file.close()
            print(f"Запись сохранена в файл {self.file_path}")
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")

        self.audio_gate.set()  # Разрешаем доступ для других операций


    def play_audio(self):
        """Прослушиваем записанный файл"""
        # Загружаем новый звук (обновляем объект SoundLoader)
        self.sound = SoundLoader.load(self.file_path)

        if self.sound:
            # Если звук загружен, воспроизводим
            self.sound.play()
            print("Проигрывание записи началось.")
        else:
            print("Не удалось загрузить звук для воспроизведения.")

    def record_chunk(self, dt):
        """Читает данные с потока и добавляет в список"""
        data = self.stream.read(1024)
        self.frames.append(data)


class AudioApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_path = "myrecording.wav"
        self.is_recording = False
        self.recorder = AudioRecorder()
        self.sound = None

    def build(self):
        return Builder.load_string(
            '''
MDScreen:

    MDRoundFlatButton:
        id: record_button
        text: "Начать запись"
        size_hint: .2, .1
        pos_hint: {"center_x": 0.5, "center_y": 0.7}
        on_release: app.toggle_recording()

    MDRoundFlatButton:
        id: play_button
        text: "Прослушать запись"
        size_hint: .2, .1
        pos_hint: {"center_x": 0.5, "center_y": 0.3}
        on_release: app.play_audio()
'''
        )

    def toggle_recording(self):
        button = self.root.ids.record_button

        if self.is_recording:
            self.is_recording = False
            button.text = "Начать запись"
            # Останавливаем запись
            self.recorder.stop_recording()
        else:
            self.is_recording = True
            button.text = "Остановить запись"
            # Начинаем запись
            self.recorder.start_recording()

    def play_audio(self):
        """Прослушиваем записанный файл"""
        # Загружаем новый звук (обновляем объект SoundLoader)
        self.sound = SoundLoader.load(self.file_path)

        if self.sound:
            # Если звук загружен, воспроизводим
            self.sound.play()
            print("Проигрывание записи началось.")
        else:
            print("Не удалось загрузить звук для воспроизведения.")


# Запуск приложения
if __name__ == "__main__":
    AudioApp().run()
