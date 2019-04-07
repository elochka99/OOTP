import os
import mutagen
import mutagen.id3
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

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

    @property
    def track_info(self):
        """
        Return track_info dictionary
        :return: track_info dictionary
        """
        return self._track_info

    @property
    def file_path(self):
        """
        Return _path to file
        :return: _path to file
        """
        return self._file_path

    def _noHeaderError(self):

        meta = mutagen.File(self._file_path, easy=True)
        for t in self.all_tag_list: #t - tag
            meta[t] = ''
        meta.save()
        return EasyID3(self._file_path)

    def _update_info(self):
        """
        Filling track_info dict with values
        """
        track = MP3(self._file_path).info.__dict__
        bitrate = str(track['bitrate'])[:3]
        length = track['length']
        sample_rate = track['sample_rate']
        track_size = os.path.getsize(self._file_path)
        track_size = track_size / 1024 / 1024
        self._track_info.update({'track_size': round(track_size, 2)})

        try:
            tag = EasyID3(self._file_path)
        except mutagen.id3.ID3NoHeaderError:
            tag = self._noHeaderError()

        tag_list = tag.keys()

        self._tag_edit_obj = tag

        self._track_info.update({'quality': '{} kbps, {} Hz'.format(bitrate,sample_rate)})

        minutes, seconds = divmod(length, 60)
        minutes, seconds = int(minutes), int(seconds)
        if seconds < 10:
            seconds = '0' + str(seconds)
        self._track_info.update({'length': '{}:{}'.format(minutes,seconds)})
        for t in self.all_tag_list:
            if t in tag_list:
                try:
                    self._track_info.update({t: tag[t][0]})
                except IndexError:
                    self._track_info.update({t: ''})
            else:
                self._track_info.update({t: ''})
