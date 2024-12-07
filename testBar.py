from kivy.core.window import Window
from kivy.lang import Builder

from kivymd.app import MDApp

Window.size = (393, 852)


class Example(MDApp):
    def build(self):
        return Builder.load_string(
            '''
MDScreen:

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
'''
        )


Example().run()