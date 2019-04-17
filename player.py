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

    def play(self):
        """
        Start playing current file.
        """
        mixer.music.play()

    def pause(self):
        """
        Pause current playing track.
        """
        mixer.music.pause()

    def unpause(self):
        """
        Continue playing current track, after pause.
        """
        mixer.music.unpause()

    def stop(self):
        """
        Stop playing current track.
        """
        mixer.music.stop()

    @property
    def volume(self):
        """
        Volume of playing
        :return: volume
        """
        return mixer.music.get_volume()

    @volume.setter
    def volume(self, volume):
        """
        Set volume
        :param volume: volume value
        """
        mixer.music.set_volume(volume)


if __name__ == '__main__':
    pass
