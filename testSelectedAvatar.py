from kivy.lang import Builder
from kivymd.app import MDApp

KV = """
MDScreen:

    MDFloatLayout:

        MDCard:
            orientation: "vertical"
            size_hint: None, None
            size: dp(180), dp(180)
            pos_hint: {"center_x": 0.5, "center_y": .8}
            radius: [dp(100),]


            FitImage:
                source: "assets/img/account.png"
                radius: [dp(100),]
                md_bg_color: 1, 1, 1, 0

    MDLabel:
        id: username_label
        text: '{app.username}'
        halign: "center"
        font_style: "H5"
        theme_font_name: "Custom"
        font_name: "assets/fonts/PTSansNarrow-Regular.ttf"
        theme_text_color: "Custom"
        text_color: "#406AAE"
        pos_hint: {"center_x": .5, "center_y": .6}

    MDLabel:
        id: useremail_label
        text: '{app.username}'
        halign: "center"
        font_style: "H5"
        theme_font_name: "Custom"
        font_name: "assets/fonts/PTSansNarrow-Regular.ttf"
        theme_text_color: "Custom"
        text_color: "#406AAE"
        pos_hint: {"center_x": .5, "center_y": .52}

    MDFillRoundFlatButton:
        text: "Выйти"
        font_style: "H5"
        font_name: "assets/fonts/PTSansCaption-Regular.ttf"
        size_hint: .55, .05
        pos_hint: {'center_x': .5, 'center_y': .2}
        theme_bg_color: "Custom"
        md_bg_color: "#AEC2EC"
        elevation_levels: dp(12)

    MDIconButton:
        icon: "arrow-left"
        style: "standard"
        pos_hint: {"center_x": .07, "center_y": .96}
"""

from kivy.core.window import Window
Window.size = (393, 852)


class testSelectedAvatar(MDApp):
    def build(self):
        return Builder.load_string(KV)


if __name__ == '__main__':
    testSelectedAvatar().run()