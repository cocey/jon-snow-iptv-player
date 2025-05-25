import types

import qtawesome as qta
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QToolBar

class PlayPauseButton:
    def __init__(self, toolBar: QToolBar = None, playFunction:types.FunctionType=None, pauseFunction:types.FunctionType=None, status="paused", state="enabled"):
        self.playIcon = qta.icon("fa6s.play")
        self.pauseIcon = qta.icon("fa6s.pause")

        self.toolBar = toolBar
        self.action = self.toolBar.addAction(self.playIcon, "Play")
        self.action.setObjectName("PlayPauseButtonAction")
        self.action.triggered.connect(self.call)

        if toolBar is None:
            raise Exception("plesase set toolBar")
        if playFunction is None:
            raise Exception("plesase set playFunction")
        if pauseFunction is None:
            raise Exception("plesase set pauseFunction")

        self.status = status
        self.state = state
        self.playFunction = playFunction
        self.pauseFunction = pauseFunction


    def getAction(self):
        return self.action

    def setStatus(self, status: str):
        self.status = status
        if status == "playing":
            self.action.setIcon(self.pauseIcon)
        elif status == "paused":
            self.action.setIcon(self.playIcon)

    def setState(self, state: str):
        self.state = state
        if state == "enabled":
            self.setEnabled()
        else:
            self.setDisabled()

    def call(self):
        if self.state == "enabled":
            if self.status == "playing" and self.pauseFunction is not None:
                self.pauseFunction()
                self.setStatus("paused")
            else:
                if self.playFunction is not None:
                    self.playFunction()
                    self.setStatus("playing")

