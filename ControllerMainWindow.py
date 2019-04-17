from viewMainWindow import MainWindow
from pattern import singleton
from PyQt5.QtWidgets import QProgressBar, QMessageBox
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

    def play(self):
        """
        use for start playing
        """
        if self.played == self.current_file_index:
            if self.bool_:
                Player().play()
                self.bool_ = False
            Player().unpause()
        else:
            Player().stop()
            Player().load(self.files[self.current_file_index].file_path)
            Player().play()

    def pause(self):
        """
        use for pause playing
        """
        Player().pause()

    def stop(self):
        """
        use for stop playing
        """
        Player().stop()
        self.bool_ = True

    def show_quit_message(self):
        """
        Show quit window.
        """
        reply = QMessageBox.question(self.ui, 'Quit massage',
                                     'Are you sure want to exit Music Tag Viever?',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.ui.close()
            self.searchDialog.ui.close()
