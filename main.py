from Circle import Circle
from Circle import importCircle

first = Circle(2022, 12, "digital", "week")
soup = first.request()

startRank = 1
endRank = 100

imp = importCircle(soup, year=2022, startRank=startRank, endRank=endRank)
SongList = imp.ImportSong()
PointList = imp.ImportPoint()
SingerList, AlbumList = imp.ImportSingerAlbum()

for i in range(startRank-1, endRank):
    print(f"{i+1:2d} : {SongList[i]:<20s} - {SingerList[i]:<20s}  |  {format(PointList[i],',')}")
