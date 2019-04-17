from viewMainWindow import MainWindow
from pattern import singleton
from PyQt5.QtWidgets import QProgressBar
from player import Player

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

    def cell_clicked(self, r, c):
        """
        When cell clicked slot.
        :param r: row
        :param c: count
        """
        item = self.ui.tracksTable.item(r, 2)
        for file in self.files:
            if item.text() == file.track_info['title']:
                self.ui.statusBar().showMessage(
                    'Track size: {} mb File path: {}'.format(file.track_info['track_size'], file.file_path)
                )
                self.current_file_index = self.files.index(file)
                self.update_tag_table(file)
                if self.bool_:
                    self.played = self.current_file_index
                    Player().load(file.file_path)
                    self.bool_ = True
