import vlc
import qtawesome as qta
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QHBoxLayout, QToolBar

from .play_pause_button import PlayPauseButton

class Player(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Player")

        self.instance = vlc.Instance()


        self.playerLayout = QVBoxLayout(self)
        self.videoFrame = QFrame()
        self.playerLayout.addWidget(self.videoFrame)

        self.mediaPlayer = self.createMediaPlayer()
        self.playerControls = self.createPlayerControls()
        self.playerLayout.addWidget(self.playerControls)



    def createMediaPlayer(self):
        mediaPlayer = self.instance.media_player_new()
        mediaPlayer.set_nsobject(self.videoFrame.winId())
        return mediaPlayer

    def createPlayerControls(self):

        toolBar = QToolBar()

        self.playPauseButton = PlayPauseButton(toolBar, self.mediaPlayer.play, self.mediaPlayer.pause)

        return toolBar


    def play(self, url:str):
        self.media = self.instance.media_new(url)
        p = self.media.parse()
        print('parse',p)
        print('get_meta',self.media.get_meta(0))
        self.mediaPlayer.set_media(self.media)
        self.mediaPlayer.play()
        self.playPauseButton.setStatus("playing")