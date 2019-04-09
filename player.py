import os
from pygame import mixer


class Player:
    def __init__(self, file_path=None):
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
