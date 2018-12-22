#!/usr/bin/env python

"""
Generate .xspf playlist file given base NGINX index URL for using with VLC.
xspf: XML Shareable Playlist Format
"""
import argparse
import bs4
import requests

argp = argparse.ArgumentParser()
argp.add_argument("baseurl", help="HTTP(S) URL to directory index")
args = argp.parse_args()

baseurl = args.baseurl.strip().strip('/')
r = requests.get(baseurl)

tree = bs4.BeautifulSoup(r.text)
tree.findAll("a")
filenames = [one.get("href") for one in tree.findAll("a") if ".mp3" in one.get("href")]

track_content = """
<track>
        <location>{}/{}</location>
        <duration>182073</duration>
        <extension application="http://www.videolan.org/vlc/playlist/0">
                <vlc:id>{}</vlc:id>
                <vlc:option>network-caching=1000</vlc:option>
        </extension>
</track>
"""

start = """\
<?xml version="1.0" encoding="UTF-8"?>
<playlist xmlns="http://xspf.org/ns/0/" xmlns:vlc="http://www.videolan.org/vlc/playlist/ns/0/" version="1">
        <title>Playlist</title>
        <trackList>
"""

end = """
        </trackList>
        <extension application="http://www.videolan.org/vlc/playlist/0">
                        <vlc:item tid="0"/>
                        <vlc:item tid="1"/>
        </extension>
</playlist>
"""
tracks = [track_content.format(baseurl, fn, idx) for idx, fn in enumerate(filenames)]

out = start + "\n".join(tracks) + end
print(out)
