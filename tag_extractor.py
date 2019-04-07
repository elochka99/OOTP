import os

class TagExtractor:
    """
    This class extract and view id3 tags in an mp3 file
    """
    def __init__(self, file_path):
        """
        Initialize the CLASS.

        :param file_path: _path to mp3 file
        """
        if not isinstance(file_path, str):
            raise ValueError('path must be str')
        if not os.path.isfile(file_path):
            raise FileNotFoundError('this path does not contain usr_input file')
        if not file_path.endswith('.mp3'):
            raise FileExistsError('this is not mp3 file')
        self._file_path = file_path
        # -- Globals. Include all information about track
        self._track_info = {}
        # all tags which must be in track_info dict
        self.all_tag_list = ['artist', 'title', 'album', 'genre', 'tracknumber',
                             'date']
        # update dict
        self._update_info()
        # if artist and title fields don`t fill
        if self._track_info['artist'] == '' and self._track_info['title'] == '':
            # artist name is "unknown"
            self._track_info['artist'] = '<unknown>'
            # title is file name without .mp3
            self._track_info['title'] = os.path.split(self._file_path)[1]
        # if track number don`t fill, replace '' to '0'
        if self._track_info['tracknumber'] == '':
            self._track_info['tracknumber'] = '0'
        # if year field don`t fill, replace '' to '0'
        if self._track_info['date'] == '':
            self._track_info['date'] = '0'

    def __str__(self):
        """
        Return track_info in user readable format
        :return: track_info in user readable format
        """
        duration = self._track_info['length']
        quality = self._track_info['quality']
        track_size = self._track_info['track_size']
        artist = self._track_info['artist']
        title = self._track_info['title']
        album = self._track_info['album']
        genre = self._track_info['genre']
        track_number = self._track_info['tracknumber']
        year = self._track_info['year']
        result = 'Track info: \nDuration: {}\nQuality: {}\nTrack size: {}\nmb\n{}\nArtist: {}'\
                 '\nTitle: {}\nAlbum: {}\nGenre: {}\nTrack number: {}\nYear: {}'\
            .format(duration, quality, track_size, '-' * 27, artist, title,
                    album, genre, track_number, year)
        return result