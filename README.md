Import your playlists to Google Play Music using simple JSON files.

This script will try to find the best match from Play Music "All Access"
library for each track.

The file format is:
{
  "playlists": [{"title": "My Playlist 1",
                 "tracks": [{"title": "My Song 1",
                             "artist": "My Artist 12",
                             "album": "My Album 42"},
                            {"title": "Meh Song 2",
                             ...}
                             ...]},
                {"title": "Mah Playlist 2",
                 "tracks": ...},
                 ...
               ]
}

This script was initially crafted to work with a Deezer playlist exporter
(https://github.com/iXce/deezerexport)

Usage
=====
Usage is straightforward:
```python2 gmusicimport.py -u USERNAME playlists.json```

You can use the `--dry-run` flag to only check the importability of the
playlists (i.e. if there are good matches for all the tracks from the All
Access library), and `-v` to increase verbosity.

Dependencies
============
We only depend on gmusicapi
(https://github.com/simon-weber/Unofficial-Google-Music-API).
which can be easily installed by running
```pip install -r requirements.txt```
or
```pip install gmusicapi```

Please note that as gmusicapi is not Python3 ready yet, this software is
Python2 only for now, though its code in itself should be Python3-compliant.
