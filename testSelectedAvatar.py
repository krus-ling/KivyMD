from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivy.uix.image import Image
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivymd.uix.gridlayout import MDGridLayout

Window.size = (393, 852)

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
                id: avatar  # Добавляем id для аватара
                source: "assets/img/avatars/account.png"
                radius: [dp(100),]
                md_bg_color: 1, 1, 1, 0
                on_touch_down: if self.collide_point(*args[1].pos): app.show_avatar_selection()

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
        on_release: app.logout_user()  # Вызываем метод выхода из аккаунта
        elevation_levels: dp(12)

    MDIconButton:
        icon: "arrow-left"
        style: "standard"
        pos_hint: {"center_x": .07, "center_y": .96}
        on_release: root.manager.current = "main"

"""


class TestChatApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.store = JsonStore("user_data.json")
        self.dialog = None
        self.selected_avatar = "assets/img/avatars/account.png"  # По умолчанию

    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        """Метод вызывается после завершения построения интерфейса"""
        # Загружаем аватар из сохранённых данных
        if self.store.exists("avatar"):
            avatar = self.store.get("avatar")["path"]
            self.selected_avatar = avatar
            if self.root:
                # Обновляем аватар только если root готов
                self.root.ids.avatar.source = avatar

    from kivy.uix.scrollview import ScrollView

    def show_avatar_selection(self):
        """Открывает диалог для выбора аватара."""
        if not self.dialog:
            # Создаем прокручиваемую область
            scroll = ScrollView(size_hint=(1, None), size=("500dp", "400dp"))

            # Сетка для отображения аватаров
            content = MDGridLayout(cols=2, spacing="30dp", size_hint_y=None)
            content.bind(minimum_height=content.setter("height"))

            # Загружаем список доступных аватаров
            avatar_paths = [
                               f"assets/img/avatars/{i}.png" for i in range(1, 12)
                           ] + ["assets/img/avatars/account.png"]

            for avatar_path in avatar_paths:
                img = Image(
                    source=avatar_path,
                    size_hint=(None, None),
                    size=("80dp", "80dp"),
                    allow_stretch=True,
                    keep_ratio=True
                )
                img.bind(
                    on_touch_down=lambda instance, touch, path=avatar_path: self.select_avatar(instance, touch, path))
                content.add_widget(img)

            # Вставляем сетку в прокручиваемую область
            scroll.add_widget(content)

            # Диалоговое окно
            self.dialog = MDDialog(
                title="Выберите аватар",
                type="custom",
                content_cls=scroll,  # Прокручиваемая область
                buttons=[
                    MDFlatButton(
                        text="Закрыть",
                        on_release=lambda x: self.dialog.dismiss(),
                    ),
                ],
            )
        self.dialog.open()

    def select_avatar(self, instance, touch, avatar_path):
        """Обрабатывает выбор аватара."""
        if instance.collide_point(*touch.pos):  # Проверяем, было ли нажатие на картинку
            print(f"Выбрана картинка по пути: {avatar_path}")
            self.selected_avatar = avatar_path
            if self.root:
                self.root.ids.avatar.source = avatar_path  # Обновляем аватар в интерфейсе
            self.save_selected_avatar()  # Сохраняем выбранный аватар
            self.dialog.dismiss()

    def save_selected_avatar(self):
        """Сохраняет выбранный аватар."""
        self.store.put("avatar", path=self.selected_avatar)
        if self.root:
            self.root.ids.avatar.source = self.selected_avatar  # Обновляем аватар в интерфейсе


if __name__ == "__main__":
    TestChatApp().run()