import sys

from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout

from player import Player

class MainWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)


        layout = QVBoxLayout()
        player = Player()
        layout.addWidget(player)
        self.setLayout(layout)

        url = "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
        player.play(url)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())