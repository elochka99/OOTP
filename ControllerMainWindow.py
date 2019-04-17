from viewMainWindow import MainWindow
from pattern import singleton
from PyQt5.QtWidgets import QProgressBar, QMessageBox, QFileDialog, QTableWidgetItem, QApplication
from player import Player
from ModelTagExtractor import TagExtractor
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import sys


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
                        self.show_web_search_dialog, self.play, self.pause,
                        self.stop, self.volume)
        self.ui.volume.setValue(int(Player().volume * 100))
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

    def show_file_dialog(self):
        """
        Displays file selection window.
        """
        self.files.clear()
        if not self.bool_:
            self.stop()
        file_name = QFileDialog.getOpenFileName(self.ui, 'Open file',
                                                '/home', '*.mp3')[0]
        if file_name:
            self.files.append(TagExtractor(file_name))
        self.update_tracks_table()

    def show_folder_dialog(self):
        """
        Displays folder selection window
        """
        self.files.clear()
        if not self.bool_:
            self.stop()
        folder_items = QFileDialog.getExistingDirectory(self.ui,
                                                        'Open folder', '/home',
                                                        QFileDialog.ShowDirsOnly
                                                        | QFileDialog.DontResolveSymlinks)
        completed = 0
        self.progressBar.setMaximumSize(180, 20)
        self.ui.statusBar().addPermanentWidget(self.progressBar)
        self.ui.statusBar().showMessage('Load songs...')
        if folder_items:
            for item in os.listdir(folder_items):
                path = folder_items + '/' + item
                if os.path.isfile(path):
                    if path.endswith('.mp3'):
                        self.files.append(
                            TagExtractor(folder_items + '/' + item))
                else:
                    continue
                self.progressBar.setValue(completed)
                completed += 100 / len(os.listdir(folder_items)) + 0.1
        self.progressBar.close()
        self.ui.statusBar().showMessage('Added' + str(len(self.files)) + ' tracks')
        self.update_tracks_table()

    def update_tag_table(self, file):
        """
        Fills the tag table with values.
        :param file: file
        """
        for count in range(1, 2):
            for row, tag in enumerate(self.tags_str_keys):
                new_item = QTableWidgetItem(file.track_info[tag])
                self.ui.tagsTable.setItem(row, count, new_item)
                if count < 2:
                    t_item = self.ui.tagsTable.item(row, count)
                    t_item.setFlags(Qt.ItemIsDragEnabled
                                    | Qt.ItemIsUserCheckable
                                    | Qt.ItemIsEnabled)

    def update_tracks_table(self):
        """
        Fills the track table with values.
        """
        self.ui.tracksTable.setRowCount(len(self.files))
        keys = ['artist', 'length', 'title']
        for r, item in enumerate(self.files):
            for c, key in enumerate(keys):
                new_item = QTableWidgetItem(item.track_info[key])
                self.ui.tracksTable.setItem(r, c, new_item)
                t_item = self.ui.tracksTable.item(r, c)
                t_item.setFlags(Qt.ItemIsDragEnabled
                                | Qt.ItemIsUserCheckable
                                | Qt.ItemIsEnabled)
                item_for_icon = self.ui.tracksTable.item(r, 0)
                item_for_icon.setIcon(QIcon('icons/song_icon.png'))

    def volume(self):
        """
        Change volume
        """
        Player().volume = round(self.ui.volume.value() / 100, 2)

    def show_web_search_dialog(self):
        """
        Slot.

        Activate web search dialog.
        """
        self.searchDialog.ui.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec())