""" https://moresound.tk """

import logging
import os
import re
import sys
import urllib.parse

import requests

import log

from .download import download
from .quality import *
from .song import Song
from .source import *

logger = logging.getLogger("log.{module_name}".format(module_name=__name__))

headers = {
    'Cookie':
    'encrypt_ip_data=3d92d85fb0b1e96245bd395599e56e614fb95f6693875f1f2ad7bc746c35e96077ab21aa0a88025f6c73ca5c0ab1d2de0b994b5a468748ae75b5a7df7fac02c8e4689c564f4e841464e7ab551d765671581eec16697a0193d35dbf52fd4409b245dd3b56c2bfc4fe7d7332c48a379d36b42ee405134fce4ad51f5d46ce416768; '
    'encrypt_data=93459ee81ef09d208bb210f996e400eaea14a8d447cbba819557bfffa2c310de52b10a383a902e20958d9bee73107681a5a43948a2d17c0cc6bcdcfa290ddfcab2c0c3b016e41eda3c5c5a651ef34dcfed25f51048e3408ba8bf8623029f42130770ad08873dfb9355d55c391f7212d5463702faec39975fd2dc51e3451f961a',
    'Content-Type':
    'application/x-www-form-urlencoded; charset=UTF-8'
}


class Moresound:
    @staticmethod
    def search(keyword, source=Source.MG, page=1, num=20):
        """Search song by keyword
        :return: totalnumber, list<Song>
        """
        if not source:
            source = Source.MG
        r = requests.session().post(
            'https://moresound.tk/music/api.php?search=' + source.value,
            'w={w}&p={p}&n={n}'.format(w=urllib.parse.quote(keyword),
                                       p=page,
                                       n=num),
            headers=headers,
        )

        json = r.json()

        id_base = num * (page - 1) + 1
        res = []
        totalnum = json['totalnum']
        for id, e in enumerate(json['song_list']):
            songname = e['songname']

            # rm html tags
            for tag in re.findall('<.+?>', e['songname']):
                songname = songname.replace(tag, '\n')

            ls = []
            for i in songname.split('\n'):
                i = i.strip()
                if i is '':
                    continue
                ls.append(i)

            songname = ls[0]
            tags = ls[1:-1]
            album = ls[-1]
            interval = e['interval'] if 'interval' in e else ''
            singer = [s['name'] for s in e['singer']
                      ] if 'singer' in e else ''  # 修正如果singer为空导致异常的情况

            token = e['songmid']

            res.append(
                Song(id_base + id, songname, singer, album, interval, tags,
                     source, token))

        return totalnum, res[:num]

    @staticmethod
    def get_download_urls(song: Song):
        logger.debug('song.source.value={0},song.token={1}'.format(
            song.source.value, song.token))
        r = requests.post(
            'https://moresound.tk/music/api.php?get_song=' + song.source.value,
            'mid={mid}'.format(mid=song.token),
            headers=headers,
        )
        json = r.json()
        logger.debug('result.json={}'.format(json))
        urls = {}
        for k, v in json['url'].items():
            try:
                r = requests.post(
                    'https://moresound.tk/music/' + v,
                    headers=headers,
                )
                urls[k] = r.json()['url']
            except:
                pass
        return urls

    @staticmethod
    def download_song(song_name, source=Source.MG, page=1, num=20):
        logger.debug('song_name={0}, source={1}'.format(song_name, source))
        total, songs = Moresound.search(song_name, source)
        if not len(songs):
            logger.error('Could not find')
            return
        urls = Moresound.get_download_urls(songs[0])
        best_quality = find_best_quality(urls)
        if not best_quality:
            logger.error('Could not find')
        singer = ','.join(songs[0].singers)
        download(
            urls[best_quality], '{singer}-{songname}.{suffix}'.format(
                singer=singer,
                songname=songs[0].name,
                suffix=get_suffix_by_quality(best_quality),
            ))


def get_vkey():
    r = requests.get(
        'https://moresound.tk/music/api.php?download=qq&004VcLEa1u2n3n/0=16c67d98bb9395fcfd239896652b0288&MS=004VcLEa1u2n3n',
        headers=headers,
    )

    url = r.json()['url']
    return url[61:61 + 112]
