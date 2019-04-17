from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic


class SearchDialog(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('search_on_web.ui', self)
        self.setWindowTitle('Search track on Web')
        self.setWindowIcon(QIcon('icons/web_search_icon.png'))
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

    def trigger(self, btn_clicked):
        self.searchButton.clicked.connect(btn_clicked)

    @property
    def web_url(self):
        return self.url.text()
