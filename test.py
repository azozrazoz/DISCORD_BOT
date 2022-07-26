import youtube_dl
options = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': u'%(id)s.%(ext)s',
    'noplaylist': True,
    'nocheckcertificate': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]
}

with youtube_dl.YoutubeDL(options) as ydl:
    # ydl.download(['https://www.youtube.com/watch?v=ohWRDgILA4o&ab_channel=doshanmusic'])
    url = 'https://www.youtube.com/playlist?list=PLe8jmEHFkvsbpE2DVU8kClkB54c-K4f3Z'
    my_json = ydl.extract_info(url, download=False)
    for el in my_json:
        print(el)
    print(ydl.extract_info(url, download=False)['title'])
