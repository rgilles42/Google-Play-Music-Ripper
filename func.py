import base64
import errno
import hmac
import os
import time
from hashlib import sha1

import eyed3  # requires to have python-magic-bin installed
import requests
import unidecode
from gmusicapi import Mobileclient


def conf(text):
    chars = """\\/:*?"<>|"""
    for c in chars:
        if c in text:
            text = text.replace(c, "_")
    return unidecode.unidecode(text)


def get_mp3(track, at, rootfolder, salt=None):
    _s1 = bytes(base64.b64decode(
        'VzeC4H4h+T2f0VI180nVX8x+Mb5HiTtGnKgH52Otj8ZCGDz9jRW''yHb6QXK0JskSiOgzQfwTY5xgLLSdUSreaLVMsVVWfxfa8Rw=='))
    _s2 = bytes(base64.b64decode(
        'ZAPnhUkYwQ6y5DdQxWThbvhJHN8msQ1rqJw0ggKdufQjelrKuiG''GJI30aswkgCWTDyHkTGK9ynlqTkJ5L4CiGGUabGeo8M6JTQ=='))
    _key = ''.join([chr(c1 ^ c2) for (c1, c2) in zip(_s1, _s2)]).encode('ascii')
    if salt is None:
        salt = str(int(time.time() * 1000))
    mac = hmac.new(_key, track['storeId'].encode('utf-8'), sha1)
    mac.update(salt.encode('utf-8'))
    sig = str(base64.urlsafe_b64encode(mac.digest())[:-1], 'utf-8')
    url = 'https://mclients.googleapis.com/music/mplay?mjck=' + track['storeId'] + '&slt=' + salt + '&sig=' + sig
    imgfilename = './' + rootfolder + '/' + conf(track['artist']) + '/' + conf(track['album']) + '/' + 'cover.jpg'
    if not os.path.exists(imgfilename):
        cover = requests.get(track['albumArtRef'][0]['url'])
        if not os.path.exists(os.path.dirname(imgfilename)):
            try:
                os.makedirs(os.path.dirname(imgfilename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open(imgfilename, "wb") as albumart:
            albumart.write(cover.content)
    print("         Downloading MP3...")
    filename = './' + rootfolder + '/' + conf(track['artist']) + '/' + conf(track['album']) + '/' + str(
        track['trackNumber']).zfill(2) + " " + conf(track['title']) + '.mp3'
    if not os.path.exists(filename):
        mp3 = requests.get(url, headers={'authorization': 'Bearer ' + at, 'x-device-id': '3695282812398831442'})
        with open(filename, "wb") as f:
            f.write(mp3.content)
    audiofile = eyed3.load(filename)
    audiofile.initTag()
    audiofile.tag.artist = track['artist']
    audiofile.tag.album = track['album']
    audiofile.tag.title = track['title']
    audiofile.tag.images.set(3, open(imgfilename, "rb").read(), "image/jpeg")
    if 'year' in track:
        audiofile.tag.release_date = track['year']
        audiofile.tag.recording_date = track['year']
    if 'genre' in track:
        audiofile.tag.genre = track['genre']
    if 'discNumber' in track:
        audiofile.tag.disc_num = (track['discNumber'], 0)
    if 'trackNumber' in track:
        audiofile.tag.track_num = track['trackNumber']
    audiofile.tag.save()
    os.remove(imgfilename)
    print("         Done !")


def search_storeid_track(track_name, at):
    data = requests.get(url="https://mclients.googleapis.com/sj/v2.5/query",
                        params={'hl': 'en_US', 'tier': 'aa', 'dv': '7938', 'ct': '1', 'q': track_name},
                        headers={'authorization': 'Bearer ' + at}).json()
    for i in range(len(data['entries'])):
        print('#' + str(i) + '      Title:' + str(data['entries'][i]['track']['title']) + '      Artist:' + str(
            data['entries'][i]['track']['artist']) + '      Album:' + str(data['entries'][i]['track']['album']))
    u = int(input("Result n°:"))
    return data['entries'][u]['track']


def performoauth():
    client = Mobileclient()
    if not os.path.exists('./oauth'):
        client.perform_oauth(storage_filepath='oauth')
    client.oauth_login(client.FROM_MAC_ADDRESS, oauth_credentials='oauth')
    return client
