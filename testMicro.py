import pyaudio
import wave
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivy.clock import Clock
import pygame

KV = '''
BoxLayout:
    orientation: 'vertical'
    size: root.width, root.height

    MDLabel:
        text: "Нажмите кнопку для записи"
        halign: 'center'
        font_style: 'H5'

    MDRaisedButton:
        text: "Начать запись"
        size_hint: None, None
        size: "200dp", "50dp"
        pos_hint: {"center_x": 0.5}
        on_release: app.start_recording()

    MDRaisedButton:
        text: "Остановить запись"
        size_hint: None, None
        size: "200dp", "50dp"
        pos_hint: {"center_x": 0.5}
        on_release: app.stop_recording()

    MDRaisedButton:
        text: "Прослушать запись"
        size_hint: None, None
        size: "200dp", "50dp"
        pos_hint: {"center_x": 0.5}
        on_release: app.play_audio()
'''


class AudioRecorderApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.recording = False

    def start_recording(self):
        """Начинает запись с микрофона."""
        self.frames = []
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=44100,
                                  input=True,
                                  frames_per_buffer=1024)
        print("Запись началась...")
        self.recording = True
        self.record_audio(0)

    def record_audio(self, dt):
        """Записывает данные с микрофона."""
        if self.recording:
            data = self.stream.read(1024)
            self.frames.append(data)
            Clock.schedule_once(self.record_audio, 0.1)

    def stop_recording(self):
        """Останавливает запись."""
        self.recording = False
        self.stream.stop_stream()
        self.stream.close()
        self.save_audio()
        print("Запись остановлена.")

    def save_audio(self):
        """Сохраняет записанное аудио в файл."""
        with wave.open("recording.wav", 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b''.join(self.frames))
        print("Аудиофайл сохранен как recording.wav")

    def play_audio(self):
        """Метод для прослушивания записи"""
        pygame.mixer.init()  # Инициализация pygame для работы с аудио
        pygame.mixer.music.load("recording.wav")  # Загружаем WAV файл
        pygame.mixer.music.play()  # Проигрываем аудио
        print("Играет аудио...")

    def on_stop(self):
        """Закрытие потока при завершении приложения."""
        if self.stream is not None:
            self.stream.close()


if __name__ == "__main__":
    AudioRecorderApp().run()
