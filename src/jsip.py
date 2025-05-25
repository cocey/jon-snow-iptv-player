import sys

from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QStackedWidget, QLabel, QHBoxLayout, QPushButton

import qtawesome as qta

from player import Player
from settings import Settings
from stream import Stream


class MainWindow(QStackedWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("MainWindow")
        self.setWindowTitle("Jon Snow Iptv Player")
        self.setMinimumWidth(480)
        self.setMinimumHeight(320)
        self.setAutoFillBackground(True)

        self.history = []
        self.stream = Stream()

        self.home = Home(stream=self.stream)
        self.addWidget(self.home)

        self.player = Player(exitFunction=self.goBack)
        self.addWidget(self.player)

        self.settings = Settings(exitFunction=self.goBack, stream=self.stream)
        self.addWidget(self.settings)

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
        if not self.stream.isLoaded:
            self.stream.load()

        self.setCurrentWidget(self.home)
        self.history.append("home")
        self.home.enableStreamMenu()

    def showPlayer(self):
        self.setCurrentWidget(self.player)
        self.history.append("player")

    def showSettings(self):
        self.setCurrentWidget(self.settings)
        self.history.append("settings")

    def showLiveTV(self):
        print("showLiveTV")

    def showMovies(self):
        print("showMovies")

    def showSeries(self):
        print("showSeries")

    def showSearch(self):
        print("showSearch")






class Home(QDialog):
    def __init__(self, parent=None, stream:Stream=None):
        super().__init__(parent)

        self.setObjectName("HomeDialog")
        self.setAutoFillBackground(True)

        self.stream = stream

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Home"))

        self.streamLayout = QHBoxLayout()

        liveButton = QPushButton(qta.icon('fa6s.tv'), 'Live TV')
        liveButton.clicked.connect(self.gotoSettings)
        self.streamLayout.addWidget(liveButton)

        moviesButton = QPushButton(qta.icon('fa6s.film'), 'Movies')
        moviesButton.clicked.connect(self.gotoSettings)
        self.streamLayout.addWidget(moviesButton)

        seriesButton = QPushButton(qta.icon('fa6s.video'), 'Series')
        seriesButton.clicked.connect(self.gotoSettings)
        self.streamLayout.addWidget(seriesButton)

        searchButton = QPushButton(qta.icon('fa6s.magnifying-glass'), 'Search')
        searchButton.clicked.connect(self.gotoSettings)
        self.streamLayout.addWidget(searchButton)

        layout.addLayout(self.streamLayout)

        menuLayout = QHBoxLayout()

        settingsButton = QPushButton(qta.icon('fa6s.gear'), 'Settings')
        settingsButton.clicked.connect(self.gotoSettings)
        menuLayout.addWidget(settingsButton)

        playSampleVideoButton = QPushButton(qta.icon('fa6s.play'), 'Play Sample Video')
        playSampleVideoButton.clicked.connect(self.playSampleVideo)
        menuLayout.addWidget(playSampleVideoButton)

        layout.addLayout(menuLayout)

        self.setLayout(layout)

    def enableStreamMenu(self):
        self.streamLayout.setEnabled(self.stream.status)

    def playSampleVideo(self):
        self.parent().showPlayer()
        self.parent().player.play("http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4")

    def gotoSettings(self):
        self.parent().showSettings()

    def gotoLiveTV(self):
        self.parent().gotoLiveTV()

    def gotoMovies(self):
        self.parent().gotoMovies()

    def gotoSeries(self):
        self.parent().gotoSeries()

    def gotoSearch(self):
        self.parent().gotoSearch()





if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())