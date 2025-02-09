from youtubesearchpython import VideosSearch
video = VideosSearch('War',region = "Ru",limit = 2)
print(video.result())
g.write(str(video.result()))