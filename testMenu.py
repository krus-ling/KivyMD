from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.screen import MDScreen


Window.size = (393, 852)


class WelcomeScreen(MDScreen):
    pass


class MainScreen(MDScreen):
    pass

KV = '''
<DrawerClickableItem@MDNavigationDrawerItem>
    focus_color: "#AEC2EC"
    text_color: "#4a4939"
    icon_color: "#4a4939"
    ripple_color: "#c5bdd2"
    selected_color: "#406AAE"


<DrawerLabelItem@MDNavigationDrawerItem>
    text_color: "#000000"
    icon_color: "#000000"
    focus_behavior: False
    selected_color: "#4a4939"
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
    
                    MDBottomNavigationItem:
                        name: 'screen 1'
                        # text: 'Mail'
                        icon: 'file-document-outline'
            
                        MDLabel:
                            text: 'История'
                            halign: 'center'
                            font_style: "H1"
            
                    MDBottomNavigationItem:
                        name: 'screen 2'
                        # text: 'Twitter'
                        icon: 'microphone-outline'
            
                        MDLabel:
                            text: 'Запись'
                            halign: 'center'
                            font_style: "H1"
            
                    MDBottomNavigationItem:
                        name: 'screen 3'
                        # text: 'Twitter'
                        icon: 'chat-outline'
            
                        MDLabel:
                            text: 'Чат'
                            halign: 'center'
                            font_style: "H1"
                # Иконка меню            
                MDIconButton:
                    icon: "assets/img/menu.png"
                    style: "standard"
                    pos_hint: {"center_x": .07, "center_y": .96}
                    on_release: nav_drawer.set_state("toggle")
            
            # Экран настроек
            MDScreen:
                name: "setting"
                
                MDLabel:
                    text: 'Настройки'
                    halign: 'center'
                    font_style: "H2"
                    
            # Экран Личного кабинета
            MDScreen:
                name: "account"
                
                MDLabel:
                    text: 'Личный кабинет'
                    halign: 'center'
                    font_style: "H2"
                    
        # Боковая панель
        MDNavigationDrawer:
            id: nav_drawer
            radius: (0, 16, 16, 0)

            MDNavigationDrawerMenu:

                DrawerClickableItem:
                    text: "Личный кабинет"
                    icon: "account-circle-outline"
                    on_release:
                        screen_manager.current = "account"
                        nav_drawer.set_state("close")

                DrawerClickableItem:
                    text: "Настройки"
                    icon: "cog-outline"
                    on_release:
                        screen_manager.current = "setting"
                        nav_drawer.set_state("close")
                        
                DrawerClickableItem:
                    text: "Выход"
                    icon: "exit-to-app"
                    on_release: app.stop()
'''


class Example(MDApp):
    def build(self):
        return Builder.load_string(KV)


Example().run()