from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic


class SearchDialog(QWidget):
    """
    This class use for displays web search dialog.
    """
    def __init__(self):
        """
        class initialization function
        """
        super().__init__()
        uic.loadUi('search_on_web.ui', self)
        self.setWindowTitle('Search track on Web')
        self.setWindowIcon(QIcon('icons/web_search_icon.png'))
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

    def trigger(self, btn_clicked):
        """
        This function shows the action by pressing the button.
        :param btn_clicked: action
        """
        self.searchButton.clicked.connect(btn_clicked)

    @property
    def web_url(self):
        """
        This function show url text
        :return: url text
        """
        return self.url.text()
