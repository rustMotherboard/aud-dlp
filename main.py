import yt_dlp
import audio_metadata
# import rgain3
import os
from pprint import pprint

def download_audio_with_metadata(url, ydl_opts):
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url)
            metadata = {
                'artist': info['uploader'],
                'album artist': info['uploader'],
                'album': info.get('album', info['title']),
                'track': info.get('track', info['title']),
                'cover_url': info['thumbnail'],
            }
            
            filename = ydl.prepare_filename(info)
            filename = process_filename(filename, ydl_opts)
        return filename,  metadata
    except Exception as e:
        print(f'An error occurred while downloading audio or extracting metadata: {e}')
        return None, None

def process_filename(filename, ydl_opts):
    filename, ext = os.path.splitext(filename)
    preferredcodec = ydl_opts['postprocessors'][0]['preferredcodec']
    filename += '.' + preferredcodec
    return filename

# def process_replaygain(filename):
#     try:
#         track = rgain3.Track(filename)
#         track.calculate_gain()
#         track.write_gain()
#     except Exception as e:
#         print(f'An error occurred while processing ReplayGain: {e}')

if __name__ == '__main__':
    url = 'https://www.youtube.com/watch?v=R3vHoL0x3GQ' # make replacable later
    ydl_opts = {
        'format': 'bestaudio', # audio only
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{ # convert to .opus via ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'opus', # make replacable later
            'preferredquality': '192',
        }],
    }
    
    filename, metadata = download_audio_with_metadata(url, ydl_opts)
    
    # if filename and metadata:
    audio_metadata.update_metadata(filename, metadata)
    #     process_replaygain(filename)