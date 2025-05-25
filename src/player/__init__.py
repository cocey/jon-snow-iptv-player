import types
import vlc
from vlc import callbackmethod
import qtawesome as qta
from PySide6.QtWidgets import QWidget, QDialog, QVBoxLayout, QFrame, QHBoxLayout, QToolBar, QPushButton, QSizePolicy, QSlider
from PySide6.QtMultimedia import QAudioOutput, QMediaFormat, QMediaPlayer, QAudio, QAudioDevice, QAudioFormat, QMediaDevices
from PySide6.QtCore import Qt, QSize, QObject, QEvent, Slot
from PySide6.QtGui import QPalette, QColor

from .play_pause_button import PlayPauseButton

class Player(QWidget):
    playerProgressScale = 1000
    volumeValue = 100
    isFullScreen = False

    def __init__(self, parent=None, exitFunction: types.FunctionType=None):
        super().__init__(parent)

        self.setObjectName("PlayerWidget")

        self.exitFunction = exitFunction

        self.instance = vlc.Instance()

        self.videoFrame = QFrame(self)
        self.videoFrame.show()

        self.mediaPlayer = self.createMediaPlayer()

        self.playerControls = self.createPlayerControls()
        self.playerControls.show()

        self.exitButton = self.createExitButton()
        self.place()
        self.installEventFilters()

    def installEventFilters(self):
        if self.window():
            self.window().setProperty('eventFilterId', 'window')
            self.window().installEventFilter(self)

        if self.parent():
            self.parent().setProperty('eventFilterId', 'parent')
            self.parent().installEventFilter(self)

        self.setProperty('eventFilterId', 'self')
        # self.installEventFilter(self)

    def eventFilter(self, watched, event):
        if watched.property("eventFilterId") in ["parent", "window"]:
            if event.type() != QEvent.Resize:
                self.place()

        return False;

    def place(self):
        if self.parent():
            self.resize(self.parent().size())

        self.videoFrame.resize(self.size())
        self.playerControls.resize(self.size().width(), self.playerControls.size().height())
        self.playerControls.move(0, self.size().height() - self.playerControls.size().height())
        if self.exitButton:
            self.exitButton.move(self.size().width() - self.exitButton.size().width(), 0)

    def createMediaPlayer(self):
        mediaPlayer = self.instance.media_player_new()
        mediaPlayer.set_nsobject(self.videoFrame.winId())
        events = mediaPlayer.event_manager()
        events.event_attach(vlc.EventType.MediaPlayerPositionChanged, self.mediaPlayerPositionChanged)
        events.event_attach(vlc.EventType.MediaPlayerPaused, self.mediaPlayerPaused)
        events.event_attach(vlc.EventType.MediaPlayerPlaying, self.mediaPlayerPlaying)


        return mediaPlayer

    @callbackmethod
    def mediaPlayerPositionChanged(self, data):
        if self.mediaPlayer.is_playing():
            value = int(self.playerProgressScale*self.mediaPlayer.get_position())
            if value >= 0:
                self.playerProgress.setValue(value)

    @callbackmethod
    def mediaPlayerPaused(self, data):
        self.playPauseButton.setStatus("paused")

    @callbackmethod
    def mediaPlayerPlaying(self, data):
        self.playPauseButton.setStatus("playing")

    def createPlayerControls(self):
        toolBar = QToolBar(self)
        toolBar.setFixedHeight(30)
        toolBar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.playPauseButton = PlayPauseButton(toolBar, self.mediaPlayer.play, self.mediaPlayer.pause)

        toolBar.addSeparator()

        self.volumeSlider = QSlider()
        self.volumeSlider.setOrientation(Qt.Orientation.Horizontal)
        self.volumeSlider.setMinimum(0)
        self.volumeSlider.setMaximum(100)
        self.volumeSlider.setFixedWidth(70)
        self.volumeSlider.setValue(self.volumeValue)
        self.volumeSlider.setTickInterval(10)
        self.volumeSlider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.volumeSlider.setToolTip("Volume")
        self.volumeSlider.valueChanged.connect(self.setVolume)
        self.volumeSlider.clearFocus()
        toolBar.addWidget(self.volumeSlider)

        toolBar.addSeparator()

        self.playerProgress = QSlider()
        self.playerProgress.setOrientation(Qt.Orientation.Horizontal)
        self.playerProgress.setMinimum(0)
        self.playerProgress.setMaximum(self.playerProgressScale)
        self.playerProgress.setTickInterval(1)
        self.playerProgress.sliderMoved.connect(self.playerProgressSliderMoved)
        self.playerProgress.sliderReleased.connect(self.playerProgressSliderReleased)
        self.playerProgress.sliderPressed.connect(self.playerProgressSliderPressed)
        toolBar.addWidget(self.playerProgress)

        toolBar.addSeparator()

        fullScreenAction = toolBar.addAction(qta.icon("fa6s.expand"), "Full Screen")
        fullScreenAction.triggered.connect(self.toggleFullScreen)


        return toolBar

    def createExitButton(self):
        if self.exitFunction:
            exitButton = QPushButton(parent=self)
            exitButton.setIcon(qta.icon("fa6s.circle-xmark"))
            exitButton.setStyleSheet("QPushButton{background-color: transparent;}")
            exitButton.clicked.connect(self.exit)
            exitButton.setIconSize(QSize(50,50))
            exitButton.setMinimumSize(50,50)
            exitButton.setMaximumSize(50,50)
            return exitButton
        return None

    @Slot()
    def setVolume(self):
        self.volumeValue = self.volumeSlider.value()
        self.mediaPlayer.audio_set_volume(self.volumeValue)

    @Slot()
    def playerProgressSliderPressed(self):
        self.mediaPlayer.pause()
        position = self.playerProgress.value()/self.playerProgressScale
        self.mediaPlayer.set_position(position)

    @Slot()
    def playerProgressSliderReleased(self):
        position = self.playerProgress.value()/self.playerProgressScale
        self.mediaPlayer.set_position(position)
        self.mediaPlayer.play()

    @Slot()
    def playerProgressSliderMoved(self):
        if not self.mediaPlayer.is_playing():
            position = self.playerProgress.value()/self.playerProgressScale
            self.mediaPlayer.set_position(position)

    @Slot()
    def toggleFullScreen(self):
        if self.isFullScreen:
            self.topLevelWidget().showNormal()
        else:
            self.topLevelWidget().showFullScreen()

        self.isFullScreen = not self.isFullScreen


    def exit(self):
        if self.exitFunction is not None:
            self.mediaPlayer.stop()
            self.exitFunction()

    def play(self, url:str):
        self.media = self.instance.media_new(url)
        p = self.media.parse()
        print('parse',p)
        print('get_meta',self.media.get_meta(0))
        self.mediaPlayer.set_media(self.media)
        self.mediaPlayer.play()
        self.playPauseButton.setStatus("playing")
        self.installEventFilters()