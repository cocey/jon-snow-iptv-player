import sys

from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QStackedWidget, QLabel, QHBoxLayout, QPushButton

import qtawesome as qta

from player import Player
from settings import Settings


class MainWindow(QStackedWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("MainWindow")
        self.setWindowTitle("Jon Snow Iptv Player")
        self.setMinimumWidth(480)
        self.setMinimumHeight(320)
        self.setAutoFillBackground(True)

        self.history = []

        self.home = Home()
        self.addWidget(self.home)

        self.player = Player(self)
        self.addWidget(self.player)

        self.settings = Settings(exitFunction=self.goBack)
        self.addWidget(self.settings)


        # url = "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
        # self.player.play(url)
        self.showHome()

    def goBack(self):
        if len(self.history) > 1:
            print(self.history)
            self.history.pop()
            self.goTo(self.history[-1])

    def goTo(self, widgetName):
        if widgetName == "home":
            self.showHome()
        elif widgetName == "player":
            self.showPlayer()
        elif widgetName == "settings":
            self.showSettings()


    def showHome(self):
        self.setCurrentWidget(self.home)
        self.history.append("home")

    def showPlayer(self):
        self.setCurrentWidget(self.player)
        self.history.append("player")

    def showSettings(self):
        self.setCurrentWidget(self.settings)
        self.history.append("settings")





class Home(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("HomeDialog")
        self.setAutoFillBackground(True)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Home"))

        menuLayout = QHBoxLayout()

        settingsButton = QPushButton(qta.icon('fa6s.gear'), 'Settings')
        settingsButton.clicked.connect(self.gotoSettings)
        menuLayout.addWidget(settingsButton)

        playSampleVideoButton = QPushButton(qta.icon('fa6s.play'), 'Play Sample Video')
        playSampleVideoButton.clicked.connect(self.playSampleVideo)
        menuLayout.addWidget(playSampleVideoButton)

        layout.addLayout(menuLayout)

        self.setLayout(layout)

    def playSampleVideo(self):
        self.parent().showPlayer()
        self.parent().player.play("http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4")

    def gotoSettings(self):
        self.parent().showSettings()





if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())