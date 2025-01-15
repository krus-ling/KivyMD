from kivy.lang import Builder
from kivy.metrics import dp
from kivy.storage.jsonstore import JsonStore
from kivymd.app import MDApp
from datetime import datetime  # Для временной метки

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

from kivy.core.window import Window
Window.size = (393, 852)

KV = """
MDScreen:

    MDNavigationLayout:

        MDScreenManager:
            id: screen_manager

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

                        MDIconButton:
                            id: action_button
                            icon: "assets/img/start_record.png"
                            icon_size: "70dp"
                            on_release: app.root.ids.bottom_nav.switch_tab("screen 3")
                            pos_hint: {"center_x": 0.5, "center_y": 0.6}

                        MDRoundFlatButton:
                            id: play_button
                            text: 'Прослушать'
                            on_release: app.playRecording()
                            disabled: True
                            pos_hint: {"center_x": 0.5, "center_y": 0.2}
                            size_hint_x: .5
                            elevation_normal: 12
                        
                        # Текстовое поле для ввода сообщений
                        MDTextField:
                            id: message_input
                            hint_text: "Введите сообщение..."
                            size_hint_y: None
                            height: "40dp"
                            pos_hint: {"center_x": 0.5, "center_y": 0.9}
                            size_hint_x: .9
                            
                        # Кнопка отправки сообщения
                        MDRaisedButton:
                            text: "Отправить"
                            size_hint_y: None
                            height: "50dp"
                            pos_hint: {"center_x": 0.5, "center_y": 0.8}
                            on_release: app.send_message(app.root.ids.message_input.text)


                    MDBottomNavigationItem:
                        name: 'screen 3'
                        icon: 'chat-outline'

                        MDBoxLayout:
                            orientation: 'vertical'
                            padding: 0
                            size_hint_y: .9
                            size_hint_x: .9
                            pos_hint: {"center_x": 0.5, "center_y": 0.45}

                            # Список сообщений
                            MDScrollView:
                                do_scroll_x: False
                                MDList:
                                    id: chat_list
                                    
                # Иконка меню
                MDIconButton:
                    icon: "menu"
                    style: "standard"
                    icon_size: "30dp"
                    theme_icon_color: "Custom"
                    icon_color: "#0c0c17"
                    pos_hint: {"center_x": .07, "center_y": .96}
                    focus_color: "#97ACD1"
                    
"""

class MessageBubble(MDBoxLayout):
    def __init__(self, message, timestamp, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None  # Высота зависит от содержимого
        self.orientation = "vertical"  # Вертикальная ориентация для текста
        self.padding = [dp(20), dp(20), dp(20), dp(20)]  # Отступы внутри фона
        self.spacing = dp(15)  # Отступы между текстом и временной меткой

        # Добавляем фон
        self.md_bg_color = "#97ACD1"  # Светлый фон
        self.radius = [dp(30), dp(30), dp(30), dp(30)]  # Радиус углов


        # Добавляем текст
        label = MDLabel(
            text=message,
            size_hint_y=.8,
            pos_hint={"center_y": .5},
            markup=True,
            halign="left",
            valign="middle",
            text_size=(self.width, None),  # Учитываем отступы
            theme_text_color="Custom",
            text_color="#FFFFFF",
        )

        label.bind(
            texture_size=lambda instance, value: setattr(self, "height", instance.texture_size[1] + 100)
        )

        # Добавляем временную метку
        timestamp_label = MDLabel(
            text=timestamp,
            size_hint_y=None,
            height=dp(5),  # Фиксированная высота
            markup=True,
            halign="right",
            valign="middle",
            text_size=(self.width - 20, None),
            theme_text_color="Custom",
            text_color="#FFFFFF",
            font_style="Caption",
        )

        self.add_widget(label)
        self.add_widget(timestamp_label)


class TestChatApp(MDApp):

    def build(self):

        # Инициализация локального хранилища
        self.store = JsonStore("user_data.json")
        self.messages_json = JsonStore("messages.json")

        return Builder.load_string(KV)

    def on_start(self):
        """Вызывается после завершения построения интерфейса"""

        saved_messages = self.load_messages()

        if not saved_messages["message"]:
            message = (
                "Тестовое сообщение раз два три."
            )
            timestamp = datetime.now().strftime("%H:%M")
            self.send_message(message, timestamp)
        else:
            # Загрузка сохранённых сообщений
            for msg in reversed(saved_messages["message"]):
                self.send_message(msg["text"], timestamp=msg["timestamp"])

        # if saved_messages:
        #     # Загрузка сообщений в правильном порядке (сначала последнее сообщение)
        #     for msg in reversed(saved_messages["message"]):
        #         self.send_message(msg["text"], timestamp=msg["timestamp"])



    def send_message(self, message="Текст-заглушка от нейронной сети", timestamp=None):
        """Отправляет сообщение в чат"""
        chat_list = self.root.ids.chat_list

        # Если временная метка не передана, используем текущее время
        if not timestamp:
            timestamp = datetime.now().strftime("%H:%M")

        # Добавляем кастомный виджет для нового сообщения
        chat_list.add_widget(MessageBubble(message=message, timestamp=timestamp), index=0)

        # Добавляем отступ между сообщениями
        chat_list.add_widget(
            MDBoxLayout(size_hint_y=None, height=30)  # Пустое пространство
        )

        # Очищаем поле ввода после отправки
        self.root.ids.message_input.text = ""

        # Прокручиваем чат вниз
        chat_list.parent.scroll_to(chat_list.children[0])

        # Сохраняем все сообщения в хранилище
        self.save_messages()

    def load_messages(self):
        """Загружает сообщения из локального хранилища JsonStore."""
        if self.messages_json.exists("messages"):
            return self.messages_json.get("messages")
        return {"message": []}

    def save_messages(self):
        """Сохраняет сообщения в локальное хранилище JsonStore."""
        messages = {"message": []}
        for message in self.root.ids.chat_list.children:
            if isinstance(message, MessageBubble):
                messages["message"].append({
                    "text": message.children[1].text,
                    "timestamp": message.children[0].text,
                })

        # Сохраняем сообщения с ключом "messages"
        self.messages_json["messages"] = messages  # Используем этот способ записи


if __name__ == '__main__':
    TestChatApp().run()
