from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem
from kivymd.uix.screen import MDScreen


Window.size = (393, 852)


class WelcomeScreen(MDScreen):
    pass


class MainScreen(MDScreen):
    pass


class BaseMDNavigationItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()


class Story(MDScreen):
    pass


class Voice(MDScreen):
    pass


class Chat(MDScreen):
    pass


class MyApp(MDApp):

    # Для переключения кнопок на нижнем NavigationBar
    def on_switch_tabs(
            self,
            bar: MDNavigationBar,
            item: MDNavigationItem,
            item_icon: str,
            item_text: str,
    ):
        self.root.ids.screen_manager.current = item_text

    def show_navigation_bar(self):
        # Делаем навигационную панель видимой
        navigation_bar = self.root.ids.navigation_bar
        navigation_bar.opacity = 1
        navigation_bar.disabled = False  # Активировать кнопки


    def build(self):
        self.theme_cls.theme_style = "Light"


        return Builder.load_file("test1.kv")


if __name__ == '__main__':
    MyApp().run()