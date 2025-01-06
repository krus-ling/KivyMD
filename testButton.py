from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen


# Загружаем интерфейс
kv = '''
MDFloatLayout:
    orientation: "vertical"

    MDIconButton:
        id: play_button
        icon: "assets/img/start_record.png"
        icon_size: "70dp"
        on_release: app.change_icon()
        # disabled: True
        pos_hint: {"center_x": 0.5, "center_y": 0.2}
        
'''

class TestButton(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.is_recording = False  # Флаг, показывающий, записываем ли мы сейчас

        return Builder.load_string(kv)

    def change_icon(self):
        # Меняем иконку при нажатии
        button = self.root.ids.play_button
        if button.icon == "assets/img/start_record.png":
            button.icon = "assets/img/stop_record.png"  # Изменить на нужную иконку
        else:
            button.icon = "assets/img/start_record.png"  # Возврат к исходной иконке


TestButton().run()
