import os
from pygame import mixer
from pattern import singleton

@singleton
class Player:
    """
    This class can play mp3 track.
    Controller mixer in PC
    """
    def __init__(self):
        """
        Initialize mixer to play music file
        """
        mixer.init()

    def load(self, file):
        """
        Initialize the class.
        :param file: _path to mp3 file
        :return: play file
        """
        if isinstance(file, str):
            if not os.path.isfile(file):
                raise FileNotFoundError('this _path does not conrain usr_input file')
            if not file.endswith('.mp3'):
                raise FileExistsError('this is not mp3 file')
        else:
            if file is not None:
                raise ValueError('_path must be str')
        mixer.music.load(file)  #load track
        return file

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