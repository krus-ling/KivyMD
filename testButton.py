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
    id: screen_manager

    WelcomeScreen:
        name: "welcome"

    MainScreen:
        name: "main"

<WelcomeScreen>:

    MDScreen:
        
        MDFloatLayout:
            orientation: 'vertical'
            md_bg_color: 1, 1, 1, 1

            
            MDCard:
                orientation: "vertical"
                md_bg_color: 1, 1, 1, 1
                pos_hint: {"center_x": .5, "center_y": .62}
                size_hint: 1, .66
            
                FitImage:
                    source: "assets/img/main.jpg"
                    
            MDLabel:
                text: "Добро пожаловать!"
                halign: "center"
                font_style: "H5"
                theme_font_name: "Custom"
                font_name: "assets/fonts/PTSansNarrow-Regular.ttf"
                pos_hint: {"center_x": .5, "center_y": .34}
            
            
            MDFillRoundFlatButton:
                text: "Начнем"
                font_style: "H5"
                font_name: "assets/fonts/PTSansCaption-Regular.ttf"
                size_hint: .55, .05
                pos_hint: {'center_x': .5, 'center_y': .2}
                theme_bg_color: "Custom"
                md_bg_color: "#AEC2EC"
                on_release: root.manager.current = "main"


<MainScreen>:

    MDScreen:
    
        MDLabel:
            text: 'Main screen'
            halign: 'center'
            font_style: "H1"
            
        MDFillRoundFlatButton:
            text: "Назад"
            font_style: "H5"
            font_name: "assets/fonts/PTSansCaption-Regular.ttf"
            size_hint: .55, .05
            pos_hint: {'center_x': .5, 'center_y': .2}
            theme_bg_color: "Custom"
            md_bg_color: "#AEC2EC"
            on_release: root.manager.current = "welcome"
''')


Example().run()