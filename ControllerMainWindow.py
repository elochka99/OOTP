from viewMainWindow import MainWindow
from pattern import singleton
from PyQt5.QtWidgets import QProgressBar

@singleton
class Main(object):
    """
    class for control Main Window
    """
    def __init__(self):
        """
        class initialization function
        """
        self.ui = MainWindow()
        self.ui.trigger(self.cell_clicked, self.show_folder_dialog,
                        self.show_file_dialog, self.show_quit_message,
                        self.show_web_search_dialog, self.play, self.pause, self.stop)
        self.files = []
        self.bool_ = False
        self.current_file_index = 0
        self.played = 0
        self.progressBar = QProgressBar()
        self.tags_str_keys = ['artist', 'title', 'album', 'genre', 'tracknumber', 'date', 'quality']
        self.ui.show()
