import sqlite3

from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.screen import MDScreen


Window.size = (393, 852)


class WelcomeScreen(MDScreen):
    pass


KV = '''
<DrawerClickableItem@MDNavigationDrawerItem>
    focus_color: "#AEC2EC"
    text_color: "#4a4939"
    icon_color: "#4a4939"
    ripple_color: "#c5bdd2"


<DrawerLabelItem@MDNavigationDrawerItem>
    text_color: "#000000"
    icon_color: "#97ACD1"
    focus_behavior: False
    _no_ripple_effect: True


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
                elevation_levels: dp(12)


MDScreen:

    MDNavigationLayout:

        MDScreenManager:
            id: screen_manager
            
            # Приветственный экран
            WelcomeScreen:
                name: "welcome"
            
            # Главный экран
            MDScreen:
                name: "main"
                
                # Навигация снизу
                MDBottomNavigation:
                    id: bottom_nav
                    selected_color_background: 0, 0, 0, 0
                    text_color_active: "#13397D"
                    text_color_normal: "#97ACD1"
            
                    MDBottomNavigationItem:
                        name: 'screen 2'
                        icon: 'microphone-outline'
                        
            
                        MDLabel:
                            text: 'Запись'
                            halign: 'center'
                            font_style: "H1"
            
                    MDBottomNavigationItem:
                        name: 'screen 3'
                        icon: 'chat-outline'
            
                        MDLabel:
                            text: 'Чат'
                            halign: 'center'
                            font_style: "H1"
                            
                # Иконка меню
                MDIconButton:
                    icon: "menu"
                    style: "standard"
                    pos_hint: {"center_x": .07, "center_y": .96}
                    focus_color: "#97ACD1"
                    on_release: nav_drawer.set_state("toggle")
            
            # Экран настроек
            MDScreen:
                name: "setting"
                
                MDLabel:
                    text: 'Темная тема'
                    halign: 'center'
                    font_style: "H4"
                    pos_hint: {"center_x": .38, "center_y": .51}
                
                MDSwitch:
                    on_active: app.on_switch_active(*args)
                    pos_hint: {"center_x": .75, "center_y": .5}
                
                MDIconButton:
                    icon: "arrow-left"
                    style: "standard"
                    pos_hint: {"center_x": .07, "center_y": .96}
                    on_release: screen_manager.current = "main"
                    
            # Экран Личного кабинета
            MDScreen:
                name: "account"
                
                MDLabel:
                    text: 'Личный кабинет'
                    halign: 'center'
                    font_style: "H2"
                
                MDIconButton:
                    icon: "arrow-left"
                    style: "standard"
                    pos_hint: {"center_x": .07, "center_y": .96}
                    on_release: screen_manager.current = "main"
                    
        # Боковая панель
        MDNavigationDrawer:
            id: nav_drawer
            radius: (0, 16, 16, 0)
            panel_color: "#97ACD1"
            
            MDBoxLayout:
                orientation: "vertical"
                padding: "8dp"
                spacing: "100dp"
                size_hint: 1, 1
            
                MDNavigationDrawerMenu:
                    MDRoundFlatIconButton:
                        id: round_flat_icon_button
                        text: "Личный кабинет"
                        icon: "account-circle-outline"
                        size_hint: .55, .5
                        line_color: [0, 0, 0, 0]
                        halign: "left"
                        text_color: "#97ACD1"
                        icon_color: "#406AAE"
                        font_size: "24sp"
                        padding: "20dp"
                        on_release:
                            screen_manager.current = "account"
                            nav_drawer.set_state("close")
    
                    MDRoundFlatIconButton:
                        text: "Настройки"
                        icon: "cog-outline"
                        size_hint: .55, .5
                        line_color: [0, 0, 0, 0]
                        halign: "left"
                        text_color: "#97ACD1"
                        icon_color: "#406AAE"
                        font_size: "24sp"
                        padding: "20dp"
                        on_release:
                            screen_manager.current = "setting"
                            nav_drawer.set_state("close")
                            
                    MDRoundFlatIconButton:
                        text: "Выход"
                        icon: "exit-to-app"
                        size_hint: .55, .5
                        line_color: [0, 0, 0, 0]
                        halign: "left"
                        text_color: "#97ACD1"
                        icon_color: "#406AAE"
                        font_size: "24sp"
                        padding: "20dp"
                        on_release: app.stop()
'''


class Example(MDApp):


    def build(self):
        self.theme_cls.theme_style = "Light"

        return Builder.load_string(KV)


    def on_switch_active(self, instance, value):
        """
        Меняет тему на темную или светлую в зависимости от состояния переключателя.
        """
        if value:  # Если переключатель активен, включаем темную тему
            self.theme_cls.theme_style = "Dark"
        else:  # Если переключатель не активен, включаем светлую тему
            self.theme_cls.theme_style = "Light"


if __name__ == "__main__":
    Example().run()