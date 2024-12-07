from kivy.core.window import Window
from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

# Window.size = (393, 852)


class WelcomeScreen(MDScreen):
    pass


class MainScreen(MDScreen):
    pass


class Example(MDApp):

    def build(self):

        return Builder.load_file("test.kv")


Example().run()