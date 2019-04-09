from pygame import mixer


class Player:
    def __init__(self, file_path=None):
        self._track_path = file_path

        mixer.init()

