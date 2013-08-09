#!/usr/bin/env python

# Copyright (C) 2013 Guillaume Seguin <guillaume@segu.in>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import getpass
import argparse
import json
from gmusicapi import Mobileclient

if __name__ == "__main__":
    client = Mobileclient()
    parser = argparse.ArgumentParser(description = 'Play Music import script')
    parser.add_argument('-u', '--user', '--username', dest = "username",
                        required = True, help = "Your username")
    parser.add_argument('-v', dest = "verbose", action = "store_true",
                        help = "Increase verbosity")
    parser.add_argument('--dry-run', dest = "dryrun", action = "store_true",
                        help = "Only perform a dry run, "
                               "don't build any playlist")
    parser.add_argument('source', metavar = "playlists.json",
                        help = "JSON file holding playlists")
    args = parser.parse_args()
    print("Logging in as \"%s\" to Google Play Music" % args.username)
    pw = getpass.getpass()
    if not client.login(args.username, pw):
        print("Authentication failed. Please check the provided credentials.")
    with open(args.source) as f:
        data = json.load(f)
    if args.dryrun:
        print "[/!\] We're currently running in dry-run mode"
    for playlist in data["playlists"]:
        if args.dryrun:
            print("Checking importability of %s" % playlist["title"])
        else:
            print("Importing %s" % playlist["title"])
        toimport = []
        for track in playlist["tracks"]:
            query = "%s %s" % (track["title"], track["artist"])
            results = client.search_all_access(query)
            match = None
            if args.verbose:
                print "Fetching matches for %s" % query
            for hit_i, hit in enumerate(results["song_hits"]):
                if hit_i >= 10:
                    break
                if args.verbose and hit_i < 10:
                    print("Hit %d, scoring %.02f: %s by %s in %s" %
                            (hit_i + 1,
                             hit["score"], hit["track"]["title"],
                             hit["track"]["artist"], hit["track"]["album"]))
                if hit["score"] > 50:
                    match = hit["track"]["storeId"]
                    break
            if match is not None:
                toimport.append(match)
            else:
                print "[!!!] No good match for %s" % query
        if not args.dryrun and toimport:
            playlist_id = client.create_playlist(playlist["title"])
            client.add_songs_to_playlist(playlist_id, toimport)
