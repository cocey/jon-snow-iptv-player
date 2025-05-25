import types

from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QVBoxLayout, QPushButton
import qtawesome as qta

class Settings(QDialog):
    def __init__(self, parent=None, exitFunction:types.FunctionType=None):
        super().__init__(parent)
        self.setObjectName("SettingsDialog")
        self.setAutoFillBackground(True)

        self.exitFunction = exitFunction

        layout = QVBoxLayout()
        self.setLayout(layout)

        backButton = QPushButton(qta.icon('fa6s.arrow-left'), 'back')
        backButton.clicked.connect(self.exit)
        layout.addWidget(backButton)

        layout.addWidget(QLabel("Username"))
        usernameInput = QLineEdit()
        layout.addWidget(usernameInput)

        layout.addWidget(QLabel("Password"))
        passwordInput = QLineEdit()
        passwordInput.setEchoMode(QLineEdit.Password)
        layout.addWidget(passwordInput)

        layout.addWidget(QLabel("Url"))
        urlInput = QLineEdit()
        layout.addWidget(urlInput)

        loginButton = QPushButton(qta.icon('fa6s.right-to-bracket'), 'Login')
        loginButton.clicked.connect(self.login)
        layout.addWidget(loginButton)

    def login(self):
        print("Login")

    def exit(self):
        if self.exitFunction is not None:
            self.exitFunction()