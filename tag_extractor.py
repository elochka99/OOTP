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
        year = self._track_info['date']
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
        # If track dond have any id3 tags, add them
        # open track as file
        meta = mutagen.File(self._file_path, easy=True)
        # add empty tags
        for t in self.all_tag_list: #t - tag
            meta[t] = ''
        # save our fie
        meta.save()
        # again open our track
        return EasyID3(self._file_path)

    def _update_info(self):
        """
        Filling track_info dict with values
        """
        # -- Track info
        # get dictionary of information about track
        track = MP3(self._file_path).info.__dict__
        # get bitrate (cut string to the desired size)
        bitrate = str(track['bitrate'])[:3]
        # get length of track (in seconds)
        length = track['length']
        # get sample rate of track (in Hz)
        sample_rate = track['sample_rate']
        # get track size in bytes
        track_size = os.path.getsize(self._file_path)
        # convert track size to mb
        track_size = track_size / 1024 / 1024
        self._track_info.update({'track_size': round(track_size, 2)})


        # -- Tag info
        # all tags which must be in track_info dict
        try:
            # get dictionary of all available tags in current track
            tag = EasyID3(self._file_path)
        except mutagen.id3.ID3NoHeaderError:
            tag = self._noHeaderError()

        # artist of available tags
        tag_list = tag.keys()

        # -- for editing
        self._tag_edit_obj = tag

        # -- Update track_info dict
        self._track_info.update({'quality': '{} kbps, {} Hz'.format(bitrate,sample_rate)})

        # convert seconds to minutes: seconds format
        minutes, seconds = divmod(length, 60)
        # convert to integer
        minutes, seconds = int(minutes), int(seconds)
        if seconds < 10:
            seconds = '0' + str(seconds)
        self._track_info.update({'length': '{}:{}'.format(minutes,seconds)})
        for t in self.all_tag_list:
            if t in tag_list:
                try:
                    self._track_info.update({t: tag[t][0]})
                except IndexError:
                    # if track tags has incorrect format
                    self._track_info.update({t: ''})
            else:
                self._track_info.update({t: ''})


if __name__ == '__main__':
    x = TagExtractor('D:/муз/76_Eminem_feat._Joyner_Lucas-Lucky_You.mp3')
    print(x)