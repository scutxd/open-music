#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os
import re
import sys

import for_lossless_music as flm
import requests

import log

logger = logging.getLogger("log.{module_name}".format(module_name=__name__))

HEADERS = {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36'
}


def fetch_playlist(url):
    logger.debug('url=' + url)

    _id = re.search(r'id=(\d+)', url).group(1)
    url = "http://music.163.com/playlist?id={0}".format(_id)
    r = requests.get(url, headers=HEADERS)
    contents = r.text
    playlist_name = re.search(r"<title>(.+)</title>", contents).group(1)[:-13]

    pattern = r'<li><a href="/song\?id=\d+">(.+?)</a></li>'
    song_list = re.findall(pattern, contents)
    if not song_list:
        logger.error('不能解析歌单 url\n')
        sys.exit(1)

    logger.info("歌单:" + playlist_name + ', 歌曲数量:{0}'.format(len(song_list)))
    logger.debug('song_list = {0}'.format(song_list))
    return song_list


def download_song_with_playlist(url,
                                source,
                                args_index,
                                page,
                                classify='--classify',
                                output_path=''):
    song_list = fetch_playlist(url)
    for song_name in song_list:
        total, songs = flm.search(song_name, source, args_index, 1)
        if not len(songs):
            print('Could not find')
            sys.exit()
        print(flm.songs2table(songs))
        urls = flm.get_download_urls(songs[0])
        best_quality = flm.find_best_quality(urls)
        if not best_quality:
            print('Could not find')
            sys.exit()
        singer = ','.join(songs[0].singers)
        input_path = os.path.abspath(output_path)
        if classify:
            input_path += '/' + singer
        os.makedirs(input_path, exist_ok=True)
        flm.download(
            urls[best_quality], '{path}/{singer}-{songname}.{suffix}'.format(
                path=input_path,
                singer=singer,
                songname=songs[0].name,
                suffix=flm.get_suffix_by_quality(best_quality),
            ))
