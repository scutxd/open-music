open-music
===================

基于comwrg的[for-lossless-music](https://github.com/comwrg/for-lossless-music)项目二次开发。新增：

- 支持咪咕音乐

feature
-------
- 可以搜索
- 可以下载
- 可以根据QQ加密格式目录下载相同歌名
- 可以自动根据歌手名分文件存储
- 加入pypi

install
-------
```
   python setup.py install
```

usage example
-------
```

   for-lossless-music 人质 #搜索歌曲人质
   for-lossless-music 人质 -i 1 -o ~/Downloads #下载搜索人质id=1的歌曲到～/Downloads目录
   for-lossless-music 人质 -i 1 -o ~/Downloads -c # 同上但是会下载到自动创建歌手文件夹中
```

todo
-------
- 可以根据一定的规则来过滤搜索
- 同时搜索几个来源，合并成一起显示
- 搜索后并不退出，可以不断的搜索并下载
- 可以从歌单下载歌曲（预计先支持QQ， 后期加入网易）

