import os
from pygame import mixer


class Player:
    """
    This class can play mp3 track.
    """
    def __init__(self, file_path=None):
        """
        Initialize the class.
        :param file_path: _path to mp3 file
        """
        if isinstance(file_path, str):
            if not os.path.isfile(file_path):
                raise FileNotFoundError('this _path does not conrain usr_input file')
            if not file_path.endswith('.mp3'):
                raise FileExistsError('this is not mp3 file')
            self._track_path = file_path
        else:
            if file_path is not None:
                raise ValueError('_path must be str')
        mixer.init()
        mixer.music.load(file_path)  #load track

    @staticmethod
    def play():
        """
        Start playing current file.
        """
        mixer.music.play()

    @staticmethod
    def pause():
        """
        Pause current playing track.
        """
        mixer.music.pause()

    @staticmethod
    def unpause():
        """
        Continue playing current track, after pause.
        """
        mixer.music.unpause()

    @staticmethod
    def stop():
        """
        Stop playing current track.
        """
        mixer.music.stop()


if __name__ == '__main__':
    pass