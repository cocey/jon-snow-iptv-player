import types
import json
import os

from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QVBoxLayout, QPushButton
import qtawesome as qta


class Settings(QDialog):
    def __init__(self, parent=None, exitFunction:types.FunctionType=None, stream=None):
        super().__init__(parent)
        self.setObjectName("SettingsDialog")
        self.setAutoFillBackground(True)

        self.exitFunction = exitFunction
        self.stream = stream

        data = self.load()
        dataLoaded = True
        if data==None:
            dataLoaded = False
            data = {
                "name": "",
                "username": "",
                "password": "",
                "url": ""
            }

        layout = QVBoxLayout()
        self.setLayout(layout)

        backButton = QPushButton(qta.icon('fa6s.arrow-left'), 'back')
        backButton.clicked.connect(self.exit)
        layout.addWidget(backButton)

        layout.addWidget(QLabel("Stream Name"))
        self.streamNameInput = QLineEdit()
        self.streamNameInput.setText(data["name"])
        layout.addWidget(self.streamNameInput)

        layout.addWidget(QLabel("Username"))
        self.usernameInput = QLineEdit()
        self.usernameInput.setText(data["username"])
        layout.addWidget(self.usernameInput)

        layout.addWidget(QLabel("Password"))
        self.passwordInput = QLineEdit()
        self.passwordInput.setEchoMode(QLineEdit.Password)
        self.passwordInput.setText(data["password"])
        layout.addWidget(self.passwordInput)

        layout.addWidget(QLabel("Url"))
        self.urlInput = QLineEdit()
        self.urlInput.setText(data["url"])
        layout.addWidget(self.urlInput)

        loginButton = QPushButton(qta.icon('fa6s.right-to-bracket'), 'Login')
        loginButton.clicked.connect(self.login)
        layout.addWidget(loginButton)

        if dataLoaded:
            self.login()
        # TODO: show status

    def login(self):
        name = self.streamNameInput.text()
        username = self.usernameInput.text()
        password = self.passwordInput.text()
        url = self.urlInput.text()

        streamLogin = self.stream.login(name, username, password, url)
        if streamLogin:
            self.save({
                "name": name,
                "username": username,
                "password": password,
                "url": url
            })

    def save(self, data):
        with open("settings.json", "w") as file:
            json.dump(data, file)

    def load(self):
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as file:
                return json.load(file)
        return None

    def exit(self):
        if self.exitFunction is not None:
            self.exitFunction()