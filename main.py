from Circle import *
from time import time

while (1):

    term = input("weekly | monthly  :  ")
    startyear, startweekmonth = map(int, input("from  :  ").split())
    endyear, endweekmonth = map(int, input("to  :  ").split())
    chart = input("digital | download | streaming  :  ")
    by = input("singer | album | song  :  ")

    chartInfo = {'startyear': startyear, 'startweekmonth':startweekmonth,
                'endyear':endyear, 'endweekmonth':endweekmonth,
                'chart':chart, 'term':term, 'by':by}

    start = time()
    imp = ChartMaking(**chartInfo)
    resultDic = imp.MakeChart()
    resultDic = imp.SortChart(resultDic)
    imp.PrintChart(resultDic)
    del imp
    end = time()

    print(f"time elapsed: {end-start}")

    k = input("continue? y/n")
    if k == 'n':
        break
    else :
        print("")

'''imp = Circle(year=2022, week=12, chart="digital", term="week", startRank=startRank, endRank=endRank)
SongList = imp.ImportSong()
PointList = imp.ImportPoint()
SingerList, AlbumList = imp.ImportSingerAlbum()

for i in range(startRank-1, endRank):
    print(f"{i+1:2d} : {SongList[i]:<20s} - {SingerList[i]:<20s}  |  {format(PointList[i],',')}")'''
