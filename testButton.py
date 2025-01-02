from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen


class TestButton(MDApp):

    def build(self):

        self.theme_cls.theme_style = "Dark"

        self.is_recording = False  # Флаг, показывающий, записываем ли мы сейчас

        return Builder.load_string(
            '''
MDScreen:

    MDRoundFlatButton:
        id: record_button
        text: "Начать запись"
        size_hint: .2, .1
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        on_release: app.toggle_recording()
''')

    def toggle_recording(self):

        # Изменяем флаг записи
        self.is_recording = not self.is_recording

        # Получаем ссылку на кнопку и меняем ее текст
        button = self.root.ids.record_button
        button.text = "Остановить запись" if self.is_recording else "Начать запись"


TestButton().run()