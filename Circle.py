from bs4 import BeautifulSoup
from selenium import webdriver
import chromedriver_autoinstaller


class Circle:
    chromedriver_autoinstaller.install()
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=CUSTOM_USER-AGENT")
    options.add_argument("headless")
    options.add_argument("disable-gpu")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2, 'plugins': 2, 'popups': 2,
                                                        'geolocation': 2, 'notifications': 2,
                                                        'auto_select_certificate': 2, 'fullscreen': 2, 'mouselock': 2,
                                                        'mixed_script': 2, 'media_stream': 2, 'media_stream_mic': 2,
                                                        'media_stream_camera': 2, 'protocol_handlers': 2,
                                                        'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2,
                                                        'push_messaging': 2, 'ssl_cert_decisions': 2,
                                                        'metro_switch_to_desktop': 2, 'protected_media_identifier': 2,
                                                        'app_banner': 2, 'site_engagement': 2, 'durable_storage': 2}}
    options.add_experimental_option('prefs', prefs)
    # https://yerintil.tistory.com/29 참조

    def __init__(self, year, weekmonth, chart, term, startRank=1, endRank=200, info=True):

        self.year = year
        self.weekmonth = "0" + str(weekmonth) if weekmonth < 10 else str(weekmonth)
        self.chart = chart
        self.term = term
        self.startRank = startRank
        self.endRank = endRank
        self.soup = self.request()
        self.info = info

    # ALL = Digital Chart |  S1020 = Download Chart | S1040 = Streaming Chart

    def makeURL(self):
        if self.term == "weekly":
            tterm = "week"
        elif self.term == "monthly":
            tterm = "month"
        ChartDic = {"digital" : "ALL", "streaming" : "S1040", "download" : "S1020"}
        URL = 'https://circlechart.kr/page_chart/onoff.circle?serviceGbn=' + ChartDic[self.chart] \
              + '&targetTime=' + self.weekmonth \
              + '&hitYear=' + str(self.year)\
              + '&termGbn=' + tterm
        return URL

    def request(self):
        driver = webdriver.Chrome(options=self.options)
        driver.implicitly_wait(1)
        driver.get(self.makeURL())
        html = driver.page_source
        return BeautifulSoup(html, 'html.parser')

    def _PointIndex(self, num):
        return '#pc_chart_tbody > tr:nth-of-type(' +str(num) + ') > td.text-center > span'

    def _SongIndex(self, num):
        return '#pc_chart_tbody > tr:nth-of-type(' +str(num) + ') > ' \
               'td:nth-of-type(3) > div > section:nth-of-type(2) > div > div.font-bold.mb-2'

    def _SingerAlbumIndex(self, num):
        return '#pc_chart_tbody > tr:nth-of-type(' +str(num) + ') > ' \
               'td:nth-of-type(3) > div > section:nth-of-type(2) > div > div.text-sm.text-gray-400.font-bold'

    def ImportPoint(self):
        point_list = []
        for i in range(self.startRank,self.endRank+1):
            point = self.soup.select(self._PointIndex(i))
            point_list.append(int(point[-1].text.translate({ord(','): ''})))
        return point_list

    def ImportSinger(self):
        singer_list = []
        for i in range(self.startRank, self.endRank+1):
            singer = self.soup.select(self._SingerAlbumIndex(i))
            singer_list.append(str(singer[-1].text).split('|', 1)[0])
        return singer_list

    def ImportAlbum(self):
        album_list = []
        for i in range(self.startRank, self.endRank+1):
            album = self.soup.select(self._SingerAlbumIndex(i))
            album_list.append(str(album[-1].text).split('|', 1)[1])
        return album_list

    def ImportSingerAlbum(self):
        singer_list = []
        album_list = []
        for i in range(self.startRank, self.endRank+1):
            tmp = self.soup.select(self._SingerAlbumIndex(i))
            singer_list.append(str(tmp[-1].text).split('|', 1)[0])
            album_list.append(str(tmp[-1].text).split('|', 1)[1])
        return singer_list, album_list

    def ImportSong(self):
        song_list = []
        for i in range(self.startRank, self.endRank+1):
            song = self.soup.select(self._SongIndex(i))
            song_list.append(str(song[-1].text))
        return song_list

    def ImportSongSingerAlbum(self):
        song_list = []
        singer_list = []
        album_list = []
        for i in range(self.startRank, self.endRank+1):
            tmp = self.soup.select(self._SingerAlbumIndex(i))
            singer_list.append(str(tmp[-1].text).split('|', 1)[0])
            album_list.append(str(tmp[-1].text).split('|', 1)[1])
            song = self.soup.select(self._SongIndex(i))
            song_list.append(str(song[-1].text))

        return song_list, singer_list, album_list

    def ImportSongWithSinger(self):
        return_list = []
        for i in range(self.startRank, self.endRank + 1):
            singer = str(self.soup.select(self._SingerAlbumIndex(i))[-1].text).split('|', 1)[0]
            song = (str(self.soup.select(self._SongIndex(i))[-1].text))
            return_list.append(song + '\t' + singer)
        return return_list

    def ImportSingerWithAlbum(self):
        return_list = []
        for i in range(self.startRank, self.endRank+1):
            singer = str(self.soup.select(self._SingerAlbumIndex(i))[-1].text).split('|', 1)[0]
            album = str(self.soup.select(self._SingerAlbumIndex(i))[-1].text).split('|', 1)[1]
            return_list.append(singer + '\t' + album)
        return return_list

class ChartMaking(Circle):

    def __init__(self, chart, term, by, startyear, startweekmonth, endyear, endweekmonth,
                 startRank = 1, endRank = 200, info=True):
        self.chart = chart
        self.term = term
        self.by = by
        self.startyear = startyear
        self.startweekmonth = startweekmonth
        self.endyear = endyear
        self.endweekmonth = endweekmonth
        self.startRank = startRank
        self.endRank = endRank
        self.year = startyear
        self.info = info
        self.weekmonth = startweekmonth



    def _request(self, year, weekmonth):
        self.year = year
        self.weekmonth = "0" + str(weekmonth) if weekmonth < 10 else str(weekmonth)
        return super().request()

    def MakeChart(self):
        byDic = {
                 'singer': super().ImportSinger,
                 'song': super().ImportSongWithSinger,
                 'album': super().ImportSingerWithAlbum
                 }

        resultDic = {}
        firstweekmonth = self.startweekmonth
        lastweekmonth = self.endweekmonth
        for year in range(self.startyear, self.endyear + 1):

            if self.term == 'weekly':
                lastweekmonth = 53 if year == 2011 or year == 2015 or year == 2016 else 52
                lastweekmonth = self.endweekmonth if year == self.endyear else lastweekmonth
            elif self.term == 'monthly':
                lastweekmonth = 12
                lastweekmonth = self.endweekmonth if year == self.endyear else lastweekmonth

            for weekmonth in range(firstweekmonth, lastweekmonth + 1):
                self.soup = self._request(year, weekmonth)
                by_list = byDic[self.by]()
                point_list = self.ImportPoint()

                for idx, point in zip(by_list, point_list):
                    if idx in resultDic:
                        resultDic[idx] += point
                    else:
                        resultDic[idx] = point
                if self.info:
                    print(f"{year} {weekmonth} done")

            firstweekmonth = 1

        return resultDic

    def SortChart(self, dict):
        sortedChart = sorted(dict.items(), key = lambda item: item[1], reverse=True)
        return sortedChart

    def PrintChart(self, list, info=True):
        if info:
            print(f"{self.startyear}.{self.startweekmonth} ~ {self.endyear}.{self.endweekmonth} "
                  f"{self.term.capitalize()} {self.chart.capitalize()} {self.by.capitalize()} Chart")

        for i, [x, y] in enumerate(list):
            print(f"{i+1:<2} : {x:<20} | {format(y,',')}")

    def __del__(self):
        print("end")


