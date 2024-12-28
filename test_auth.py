import re
import sqlite3


from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.screen import MDScreen

from kivy.core.window import Window
Window.size = (393, 852)


# Создаем подключение к SQLite
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


class LoginScreen(MDScreen):
    pass


class WelcomeScreen(MDScreen):
    pass


class RegisterScreen(MDScreen):
    pass


class MainApp(MDApp):
    dialog = None
    password_visible = False  # Статус видимости пароля

    def build(self):
        self.title = "Авторизация и регистрация"
        init_db()
        return Builder.load_string(KV)

    def login_user(self, identifier, password):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM users WHERE (username = ? OR email = ?) AND password = ?
        """, (identifier, identifier, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            self.show_dialog("Успех", f"Добро пожаловать, {user[1]}!")  # user[1] — имя пользователя
            self.root.current = "welcome"  # Переход на WelcomeScreen

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


# KV-код
KV = """
MDScreenManager:
    id: screen_manager
    LoginScreen:
        name: "login"
    RegisterScreen:
        name: "register"
    WelcomeScreen:
        name: "welcome"


<LoginScreen>:
    
    MDCard:
        orientation: "vertical"
        md_bg_color: 1, 1, 1, 0
        size_hint: .7, 1
        
        FitImage:
            source: "assets/img/auth_bg.png"
            pos_hint: {"center_x": .93}

    MDFloatLayout:
    
        MDLabel:
            text: "Авторизация"
            color: "#6A7895"
            theme_font_name: "Custom"
            font_name: "assets/fonts/PTSansCaption-Regular.ttf"
            pos_hint: {"center_x": 0.5, "center_y": 0.83}
            halign: "center"
            font_style: "H5"
        
        MDFillRoundFlatButton:
            text: "Войти"
            font_style: "H5"
            font_name: "assets/fonts/PTSansCaption-Regular.ttf"
            size_hint: .55, .05
            pos_hint: {"center_x": 0.5, "center_y": 0.3}
            theme_bg_color: "Custom"
            md_bg_color: "#AEC2EC"
            on_release: app.login_user(identifier.text, password.text)
            
        MDRoundFlatButton:
            text: "Зарегистрироваться"
            line_color: [1, 1, 1, 0]
            text_color: [0, 0, 0, 1]
            pos_hint: {"center_x": 0.5, "center_y": 0.24}
            on_release: root.manager.current = "register"

        
            
        MDBoxLayout:
            orientation: "vertical"
            size_hint: 0.9, .2
            height: self.minimum_height
            pos_hint: {"center_x": 0.55, "center_y": 0.65}
            spacing: dp(20)
            padding: dp(10)

            MDTextField:
                id: identifier
                hint_text: "*Почта или логин"
                
                color_mode: 'Custom'
                line_color_focus: "#6A7895"
                

            MDBoxLayout:
                orientation: "horizontal"
                size_hint_y: .4
                

                MDTextField:
                    id: password
                    hint_text: "*Пароль"
                    password: True
                    size_hint_x: 0.8
                    line_color_focus: "#6A7895"

                MDIconButton:
                    id: toggle_password_auth
                    icon: 'eye-off'
                    size_hint_x: 0.2
                    on_release: app.toggle_password_visibility_auth(password, toggle_password_auth)
                



<RegisterScreen>:

    MDFloatLayout:

        MDCard:
            orientation: "vertical"
            md_bg_color: 1, 1, 1, 0
            size_hint: .7, 1

            FitImage:
                source: "assets/img/auth_bg.png"
                pos_hint: {"center_x": .93}

        MDLabel:
            text: "Регистрация"
            color: "#6A7895"
            theme_font_name: "Custom"
            font_name: "assets/fonts/PTSansCaption-Regular.ttf"
            pos_hint: {"center_x": 0.5, "center_y": 0.83}
            halign: "center"
            font_style: "H5"

        MDFillRoundFlatButton:
            text: "Зарегистрироваться"
            font_style: "Subtitle1"
            font_name: "assets/fonts/PTSansCaption-Regular.ttf"
            size_hint: .55, .05
            pos_hint: {"center_x": 0.5, "center_y": 0.25}
            theme_bg_color: "Custom"
            md_bg_color: "#AEC2EC"
            on_release: app.register_user(reg_username.text, reg_email.text, reg_password.text, password_repeat.text)

        MDRoundFlatButton:
            text: "Назад ко входу"
            pos_hint: {"center_x": 0.5, "center_y": 0.19}
            line_color: [1, 1, 1, 0]
            text_color: [0, 0, 0, 1]
            on_release: root.manager.current = "login"


        MDBoxLayout:
            orientation: "vertical"
            size_hint: 0.9, .4
            height: self.minimum_height
            pos_hint: {"center_x": 0.55, "center_y": 0.55}
            spacing: dp(20)
            padding: dp(10)

            MDTextField:
                id: reg_username
                hint_text: "*Логин"
                line_color_focus: "#6A7895"
                max_text_length: 20
                size_hint_x: 0.8
            MDTextField:
                id: reg_email
                hint_text: "*Почта"
                line_color_focus: "#6A7895"
                size_hint_x: 0.8

            MDBoxLayout:
                orientation: "horizontal"
                size_hint_y: .4

                MDTextField:
                    id: reg_password
                    hint_text: "*Пароль"
                    password: True
                    line_color_focus: "#6A7895"
                    size_hint_x: 0.8

                MDIconButton:
                    id: toggle_password_reg
                    icon: 'eye-off'
                    size_hint_x: 0.2
                    on_release: app.toggle_password_visibility_reg(reg_password, password_repeat, toggle_password_reg)

            MDTextField:
                id: password_repeat
                hint_text: "*Повторите пароль"
                password: True
                line_color_focus: "#6A7895"
                size_hint_x: 0.8

            


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
"""

if __name__ == "__main__":
    MainApp().run()
