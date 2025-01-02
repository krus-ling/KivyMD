'''
android.permissions = RECORD_AUDIO, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

requirements = python3,
    kivy,
    kivymd,
    materialyoucolor,
    exceptiongroup,
    asyncgui,
    asynckivy,
    jnius
'''

import os

from android.permissions import request_permissions, Permission
from jnius import autoclass
from kivy.clock import Clock
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout

Builder.load_string('''
<AudioTool>

    MDFloatLayout:
        orientation: "vertical"
        
        MDLabel:
            id: display_label
            text: 'Click on the button'
            pos_hint: {"center_x": 0.5, "center_y": .8}
            halign: "center"
    
        MDRoundFlatButton:
            id: start_button
            text: 'Start Recording'
            on_release: root.startRecording_clock()
            pos_hint: {"center_x": 0.5, "center_y": 0.6}
    
        MDRoundFlatButton:
            id: stop_button
            text: 'Stop Recording'
            on_release: root.stopRecording()
            disabled: True
            pos_hint: {"center_x": 0.5, "center_y": 0.4}
    
        MDRoundFlatButton:
            id: play_button
            text: 'Play Recording'
            on_release: root.playRecording()
            disabled: True
            pos_hint: {"center_x": 0.5, "center_y": 0.2}
''')


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
        request_permissions([
            Permission.RECORD_AUDIO,
            Permission.WRITE_EXTERNAL_STORAGE,
            Permission.READ_EXTERNAL_STORAGE
        ])
        return AudioTool()


class AudioTool(MDFloatLayout):
    def __init__(self, **kwargs):
        super(AudioTool, self).__init__(**kwargs)

        self.start_button = self.ids['start_button']
        self.stop_button = self.ids['stop_button']
        self.display_label = self.ids['display_label']
        self.play_button = self.ids['play_button']
        self.player = None  # Объект MediaPlayer


    def startRecording_clock(self):

        self.start_button.disabled = True  # Prevents the user from clicking start again which may crash the program
        self.stop_button.disabled = False
        Clock.schedule_once(self.startRecording)  ## NEW start the recording

    def startRecording(self, dt):  # NEW start the recorder
        self.r = MyRecorder()
        self.r.mRecorder.start()
        self.play_button.disabled = True  # Отключаем кнопку во время записи
        self.display_label.text = "Recording..."

    def stopRecording(self):

        self.r.mRecorder.stop()  # NEW RECORDER VID 6
        self.r.mRecorder.release()  # NEW RECORDER VID 6

        Clock.unschedule(self.startRecording)  # NEW stop the recording of audio VID 6
        self.start_button.disabled = False
        self.stop_button.disabled = True  # TUT 3

        # Активируем кнопку воспроизведения
        self.play_button.disabled = False

        self.display_label.text = "Recording completed"

    def playRecording(self):
        if not self.player:
            self.player = MyPlayer()  # Создаём объект MyPlayer
            self.player.set_data_source(self.r.get_output_file())  # Устанавливаем источник данных (путь к файлу)
            self.player.prepare()  # Подготавливаем для воспроизведения
        self.player.start()  # Запускаем воспроизведение

        # Событие по завершению воспроизведения
        self.player.set_on_completion_listener(lambda mp: self.onPlaybackComplete())

    def onPlaybackComplete(self):
        '''Сбрасываем состояние после завершения воспроизведения'''
        self.display_label.text = "Playback Finished!"
        self.player.release()
        self.player = None


if __name__ == '__main__':
    AudioApp().run()