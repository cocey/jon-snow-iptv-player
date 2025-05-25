import types
import json
from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QVBoxLayout, QPushButton, QHBoxLayout, QWidget, QScrollArea
from PySide6.QtCore import Qt, Slot
import qtawesome as qta


class Search(QDialog):
    def __init__(self, parent=None, exitFunction:types.FunctionType=None, stream=None):
        super().__init__(parent)
        self.setObjectName("SearchDialog")
        self.setAutoFillBackground(True)

        self.exitFunction = exitFunction
        self.stream = stream

        layout = QVBoxLayout()
        self.setLayout(layout)

        topLayout = QHBoxLayout()

        topLayout.addWidget(QLabel("Search"))
        self.inputSearch = QLineEdit()
        self.inputSearch.returnPressed.connect(self.search)
        topLayout.addWidget(self.inputSearch)

        backButton = QPushButton(qta.icon('fa6s.arrow-left'), 'back')
        backButton.clicked.connect(self.exit)
        topLayout.addWidget(backButton)

        layout.addLayout(topLayout)

        self.channelsLayout = QVBoxLayout()
        scrollAreaContent = QWidget()
        scrollAreaContent.setLayout(self.channelsLayout)

        scrollArea = QScrollArea()
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(scrollAreaContent)

        layout.addWidget(scrollArea)

        if not self.stream.isLoaded:
            self.stream.load()

        self.updateList(self.stream.getData())

    def exit(self):
        if self.exitFunction is not None:
            self.exitFunction()

    @Slot()
    def search(self):
        result = self.stream.search(self.inputSearch.text())
        self.updateList(result)

    def updateList(self, data):
        #clear list
        while self.channelsLayout.count():
            item = self.channelsLayout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for section in data:
            self.channelsLayout.addWidget(QLabel(section))
            i = 0
            for item in data[section]:
                button = QPushButton(item["name"])
                button.setStyleSheet("text-align:left;")
                button.setObjectName(json.dumps(item))
                button.clicked.connect(self.setChannel)
                self.channelsLayout.addWidget(button)
                i+=1
                if i>100:
                    break

    @Slot()
    def setChannel(self):
        btn = self.sender()
        item = json.loads(btn.objectName())
        print("setChannel", item)

        if item["type"]=="serie":
            self.updateList(self.stream.getSerie(item["id"]))
        else:
            self.parent().play(item["url"])