import yt_dlp

# Configure yt-dlp and obtain metadata
URL = 'https://www.youtube.com/watch?v=R3vHoL0x3GQ'
ydl_opts = {}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(URL, download=False) # audio could be download while obtaining metadata

# Allocate Metadata Items 
artist = info['uploader']
album = info.get('album', info['title'])
track = info.get('track', info['title'])
thumbnail_url = info['thumbnail']

# Print Metadata Items
print(f'''
Artist: {artist}
Album: {album}
Track: {track}
Thumbnail URL: {thumbnail_url}
''')