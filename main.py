from kivy.core.window import Window
from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

Window.size = (393, 852)


class WelcomeScreen(MDScreen):
    pass


class App(MDApp):

    def build(self):

        self.theme_cls.theme_style = "Light"

        return Builder.load_file("main.kv")


    def on_switch_active(self, instance, value):
        """
        Меняет тему на темную или светлую в зависимости от состояния переключателя.
        """
        if value:  # Если переключатель активен, включаем темную тему
            self.theme_cls.theme_style = "Dark"
        else:  # Если переключатель не активен, включаем светлую тему
            self.theme_cls.theme_style = "Light"


if __name__ == '__main__':
    App().run()