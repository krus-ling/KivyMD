import re
import sqlite3


from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import BooleanProperty, StringProperty
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen

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

    # Флаг авторизации и данные пользователя
    is_logged_in = BooleanProperty(False)
    username = StringProperty("")
    email = StringProperty("")

    def build(self):

        self.theme_cls.theme_style = "Light"

        return Builder.load_file("test.kv")

    def login_user(self, identifier, password):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM users WHERE (username = ? OR email = ?) AND password = ?
        """, (identifier, identifier, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            self.is_logged_in = True
            self.username = user[1]  # Имя пользователя
            self.email = user[2]  # Почта пользователя

            # Обновляем текст на экране Личного кабинета
            self.root.ids.screen_manager.get_screen(
                'account').ids.username_label.text = self.username  # Логин

            self.root.ids.screen_manager.get_screen(
                'account').ids.useremail_label.text = self.email  # Почта


            self.show_dialog("Успех", f"Добро пожаловать, {user[1]}!")  # user[1] — имя пользователя
            self.root.ids.screen_manager.current = "account"  # Переход в личный кабинет

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

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
            conn.commit()
            self.show_dialog("Успех", "Регистрация успешна!")
            self.root.ids.screen_manager.current = "login"  # Переход ко входу

        except sqlite3.IntegrityError:
            self.show_dialog("Ошибка", "Пользователь с таким именем или почтой уже существует.")
        finally:
            conn.close()

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