'''
android.permissions = RECORD_AUDIO, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, INTERNET

requirements = python3,
    kivy,
    kivymd,
    materialyoucolor,
    exceptiongroup,
    asyncgui,
    asynckivy,
    jnius
    mysql-connector-python,
    python-dotenv
'''

import os

from android.permissions import request_permissions, Permission
from jnius import autoclass
from kivy.clock import Clock
from kivy.lang import Builder
from kivymd.app import MDApp

# Загружаем интерфейс
kv = '''
MDFloatLayout:
    orientation: "vertical"

    MDLabel:
        id: display_label
        text: 'Нажми на кнопку'
        pos_hint: {"center_x": 0.5, "center_y": .8}
        halign: "center"
        size_hint_x: .8

    MDRoundFlatButton:
        id: action_button
        text: 'Начать запись'
        on_release: app.toggleRecording()
        pos_hint: {"center_x": 0.5, "center_y": 0.6}
        size_hint_x: .5

    MDRoundFlatButton:
        id: play_button
        text: 'Прослушать'
        on_release: app.playRecording()
        disabled: True
        pos_hint: {"center_x": 0.5, "center_y": 0.2}
        size_hint_x: .5
'''


class MyRecorder:
    def __init__(self):
        '''Recorder object To access Android Hardware'''
        self.MediaRecorder = autoclass('android.media.MediaRecorder')
        self.AudioSource = autoclass('android.media.MediaRecorder$AudioSource')
        self.OutputFormat = autoclass('android.media.MediaRecorder$OutputFormat')
        self.AudioEncoder = autoclass('android.media.MediaRecorder$AudioEncoder')

        # create out recorder
        self.mRecorder = self.MediaRecorder()
        self.mRecorder.setAudioSource(self.AudioSource.MIC)
        self.mRecorder.setOutputFormat(self.OutputFormat.THREE_GPP)

        # Используем безопасный путь для записи
        Context = autoclass('android.content.Context')
        activity = autoclass('org.kivy.android.PythonActivity').mActivity
        storage_path = activity.getExternalFilesDir(None).getAbsolutePath()
        if not storage_path:
            raise Exception("Не удалось получить путь для сохранения файла.")
        os.makedirs(storage_path, exist_ok=True)


        self.output_file = os.path.join(storage_path, "MYAUDIO.3gp")
        self.mRecorder.setOutputFile(self.output_file)
        self.mRecorder.setAudioEncoder(self.AudioEncoder.AMR_NB)
        self.mRecorder.prepare()

    def get_output_file(self):
        '''Возвращает путь к сохранённому аудиофайлу'''
        return self.output_file


class MyPlayer:
    def __init__(self):
        """Player object to play the audio file using Android hardware"""
        self.MediaPlayer = autoclass('android.media.MediaPlayer')

        # Создаём объект MediaPlayer
        self.mPlayer = self.MediaPlayer()

    def set_data_source(self, file_path):
        '''Устанавливает источник данных для воспроизведения'''
        self.mPlayer.setDataSource(file_path)

    def prepare(self):
        '''Готовит MediaPlayer к воспроизведению'''
        self.mPlayer.prepare()

    def start(self):
        '''Запускает воспроизведение'''
        self.mPlayer.start()

    def stop(self):
        '''Останавливает воспроизведение'''
        self.mPlayer.stop()

    def release(self):
        '''Освобождает ресурсы MediaPlayer'''
        self.mPlayer.release()

    def set_on_completion_listener(self, listener):
        '''Устанавливает слушатель завершения воспроизведения'''
        self.mPlayer.setOnCompletionListener(listener)


class AudioApp(MDApp):
    def build(self):
        # Запрос разрешений при запуске приложения
        request_permissions([Permission.RECORD_AUDIO,
                             Permission.WRITE_EXTERNAL_STORAGE,
                             Permission.READ_EXTERNAL_STORAGE])
        return Builder.load_string(kv)

    def on_start(self):
        self.is_recording = False  # Флаг для отслеживания состояния записи
        self.player = None  # Объект MediaPlayer

    def toggleRecording(self):
        '''Toggle recording state'''
        if self.is_recording:
            self.stopRecording()
        else:
            self.startRecording_clock()

    def startRecording_clock(self):
        Clock.schedule_once(self.startRecording)

    def startRecording(self, dt):
        self.r = MyRecorder()
        self.r.mRecorder.start()
        self.is_recording = True
        self.root.ids.action_button.text = 'Остановить запись'
        self.root.ids.play_button.disabled = True  # Отключаем кнопку во время записи
        self.root.ids.display_label.text = "Запись..."

    def stopRecording(self):
        self.r.mRecorder.stop()
        self.r.mRecorder.release()

        self.is_recording = False
        self.root.ids.action_button.text = 'Начать запись'
        self.root.ids.display_label.text = "Сообщение записано"

        # Активируем кнопку воспроизведения
        self.root.ids.play_button.disabled = False

    def playRecording(self):
        if not self.player:
            self.player = MyPlayer()
            self.player.set_data_source(self.r.get_output_file())  # Устанавливаем источник данных (путь к файлу)
            self.player.prepare()  # Подготавливаем для воспроизведения
        self.player.start()  # Запускаем воспроизведение

        # Событие по завершению воспроизведения
        self.player.set_on_completion_listener(lambda mp: self.onPlaybackComplete())

    def onPlaybackComplete(self):
        '''Сбрасываем состояние после завершения воспроизведения'''
        self.root.ids.display_label.text = "Запись прослушана!"
        self.player.release()
        self.player = None


if __name__ == '__main__':
    AudioApp().run()