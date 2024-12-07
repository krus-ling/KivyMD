from kivy.core.window import Window
from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

Window.size = (393, 852)


class WelcomeScreen(MDScreen):
    pass


class MainScreen(MDScreen):
    pass


class Example(MDApp):

    def build(self):
        self.theme_cls.primary_palette = 'Red'

        return Builder.load_string(
            '''
MDScreenManager:
    WelcomeScreen:

<WelcomeScreen>:
    MDScreen:
        Button:
            text: "Нажми меня"
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            size_hint: 0.5, 0.1
''')

Example().run()
