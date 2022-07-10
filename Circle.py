from bs4 import BeautifulSoup
from selenium import webdriver
import chromedriver_autoinstaller


class Circle:
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=CUSTOM_USER-AGENT")
    options.add_argument("headless")
    options.add_argument("disable-gpu")

    def __init__(self, year, week, chart, term):
        self.year = year
        self.week = "0" + str(week) if week < 10 else str(week)
        self.chart = chart
        self.term = term
        chromedriver_autoinstaller.install()

    # ALL = Digital Chart |  S1020 = Download Chart | S1040 = Streaming Chart

    def makeURL(self):
        ChartDic = {"digital" : "ALL", "streaming" : "S1040", "download" : "S1020"}
        URL = 'https://circlechart.kr/page_chart/onoff.circle?serviceGbn=' + ChartDic[self.chart] \
              + '&targetTime=' + self.week \
              + '&hitYear=' + str(self.year)\
              + '&termGbn=' + self.term
        return URL

    def request(self):
        driver = webdriver.Chrome(options=self.options)
        driver.implicitly_wait(2)
        driver.get(self.makeURL())
        html = driver.page_source
        return BeautifulSoup(html, 'html.parser')



class importCircle:

    def __init__(self, soup, year, startRank, endRank):
        self.soup = soup
        self.year = year
        self.startRank = startRank
        self.endRank = endRank

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



