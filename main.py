


import json
import re

import mysql.connector
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import BooleanProperty, StringProperty
from kivy.storage.jsonstore import JsonStore
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen

with open('config.json') as config_file:
    config = json.load(config_file)

Window.size = (393, 852)


class LoginScreen(MDScreen):
    pass


class RegisterScreen(MDScreen):
    pass


class WelcomeScreen(MDScreen):
    pass


class SettingsScreen(MDScreen):
    pass


class AccountScreen(MDScreen):
    pass


class App(MDApp):

    dialog = None
    password_visible = False  # Статус видимости пароля
    conn = None  # Атрибут для хранения соединения с БД
    store = None  # Хранилище для сохранения состояния входа

    # Флаг авторизации и данные пользователя
    is_logged_in = BooleanProperty(False)
    username = StringProperty("")
    email = StringProperty("")

    def build(self):

        self.theme_cls.theme_style = "Light"

        # Инициализация локального хранилища
        self.store = JsonStore("user_data.json")

        # Установить соединение с БД при запуске
        self.conn = mysql.connector.connect(
            host=config["host"],
            user = config["user"],
            password = config["password"],
            database = config["database"]
        )

        return Builder.load_file("test.kv")

    def on_start(self):

        # Проверить, сохранено ли состояние входа
        if self.store.exists("user"):
            user_data = self.store.get("user")
            self.username = user_data["username"]
            self.email = user_data["email"]
            self.is_logged_in = True

            # Переключаемся на экран Личного кабинета после загрузки интерфейса
            self.root.ids.screen_manager.current = "account"

            # Обновляем текст на экране Личного кабинета
            self.root.ids.screen_manager.get_screen('account').ids.username_label.text = self.username
            self.root.ids.screen_manager.get_screen('account').ids.useremail_label.text = self.email

    def login_user(self, identifier, password):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT * FROM users WHERE (username = %s OR email = %s) AND password = %s
        """, (identifier, identifier, password))
        user = cursor.fetchone()

        if user:
            self.is_logged_in = True
            self.username = user[1]  # Имя пользователя
            self.email = user[2]  # Почта пользователя

            # Сохраняем состояние входа
            self.store.put("user", username=self.username, email=self.email)

            # Обновляем текст на экране Личного кабинета
            self.root.ids.screen_manager.get_screen('account').ids.username_label.text = self.username  # Логин
            self.root.ids.screen_manager.get_screen('account').ids.useremail_label.text = self.email  # Почта

            self.show_dialog("Успех", f"Добро пожаловать, {user[1]}!")  # user[1] — имя пользователя
            self.root.ids.screen_manager.current = "account"  # Переход в личный кабинет

            self.conn.close()

        else:
            self.show_dialog("Ошибка", "Неверная почта или пароль.")

    def register_user(self, username, email, password, password_repeat):

        # Проверяем, что все поля заполнены
        if not username or not email or not password:
            self.show_dialog("Ошибка", "Заполните все поля.")
            return

        # Проверяем длину логина
        if len(username) > 20:
            self.show_dialog("Ошибка", "Логин должен быть не больше 20 символов.")
            return

        # Проверяем валидность почты
        if not self.is_valid_email(email):
            self.show_dialog("Ошибка", "Некорректная почта.")
            return

        # Если пароли не совпадают, выводим сообщение об ошибке
        if password != password_repeat:
            self.show_dialog("Ошибка", "Пароли не совпадают.")
            return

        cursor = self.conn.cursor()

        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
            self.conn.commit()
            self.show_dialog("Успех", "Регистрация успешна!")
            self.root.ids.screen_manager.current = "login"  # Переход ко входу

        except mysql.connector.IntegrityError:
            self.show_dialog("Ошибка", "Пользователь с таким именем или почтой уже существует.")

    def logout_user(self):

        """
        Метод для выхода из аккаунта.
        """

        if not self.conn or not self.conn.is_connected():
            self.conn = mysql.connector.connect(
                host=config["host"],
                user=config["user"],
                password=config["password"],
                database=config["database"]
            )

        self.is_logged_in = False
        self.username = ""
        self.email = ""

        # Удаляем сохранённое состояние
        if self.store.exists("user"):
            self.store.delete("user")

        # Очистить поля ввода на экране входа
        login_screen = self.root.ids.screen_manager.get_screen('login')
        login_screen.ids.identifier.text = ""  # Очищаем поле для имени пользователя или email
        login_screen.ids.password.text = ""  # Очищаем поле для пароля

        # Возвращаемся на экран входа
        self.root.ids.screen_manager.current = "login"



    def show_dialog(self, title, text):
        if not self.dialog:
            self.dialog = MDDialog(
                title=title,
                text=text,
                buttons=[MDFlatButton(text="OK", on_release=self.close_dialog)],
            )
        self.dialog.title = title
        self.dialog.text = text
        self.dialog.open()


    # Метод для переключения видимости пароля в регистрации
    def toggle_password_visibility_reg(self, password_field, repeat_password_field, button):
        self.password_visible = not self.password_visible
        password_field.password = not self.password_visible  # Меняем видимость пароля
        repeat_password_field.password = not self.password_visible  # Меняем видимость повторного пароля
        button.icon = "eye" if self.password_visible else "eye-off"  # Меняем иконку кнопки

    # Метод для переключения видимости пароля в авторизации
    def toggle_password_visibility_auth(self, textfield, button):
        self.password_visible = not self.password_visible
        textfield.password = not self.password_visible
        button.icon = "eye" if self.password_visible else "eye-off"



    @staticmethod
    def is_valid_email(email):
        """
        Проверяет валидность почтового адреса
        Возвращает True, если адрес валидный, иначе False
        """
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(pattern, email) is not None


    def close_dialog(self, *args):
        self.dialog.dismiss()


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