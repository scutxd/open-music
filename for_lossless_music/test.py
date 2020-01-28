import unittest
import for_lossless_music as flm


class Test(unittest.TestCase):
    def test_fetch_playlist(self):
        correct_url = 'https://music.163.com/#/playlist?id=2594603185'

        correct_url_songlist = [
            'Careless Whisper', 'Be Free', 'How Long Will I Love You',
            'Wham Bam Shang-A-Lang', 'California Dreaming (重庆森林)',
            'Talk Baby Talk', '水边的阿狄丽娜', 'Levels', 'Ode an die Freude',
            'Let Me Know'
        ]
        wrong_url = "id=22"

        self.assertEqual(len(flm.fetch_playlist(correct_url)), 10)
        self.assertCountEqual(flm.fetch_playlist(correct_url),
                              correct_url_songlist)
        with self.assertRaises(SystemExit) as cm:
            flm.fetch_playlist(wrong_url)
        self.assertEqual(cm.exception.code, 1)

    def test_download_song(self):
        # flm.download_song('不谓侠', flm.Source.MG)
        # flm.download_song('Wham Bam Shang-A-Lang', flm.Source.MG)
        flm.download_song('Levels', flm.Source.MG)

    def test_download_all_songs_in_playlist(self):
        correct_url = 'https://music.163.com/#/playlist?id=2594603185'
        flm.download_all_songs_in_playlist(correct_url, flm.Source.MG)


if __name__ == '__main__':
    unittest.main()
