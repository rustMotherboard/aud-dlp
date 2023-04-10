from mutagen import File
import requests
from io import BytesIO
# from PIL import Image

def get_metadata(filename: str):
    # wip. might be needed for the GUI
    pass

def get_image_cover(url: str):
    raw_img = requests.get(url, stream=True)
    img = BytesIO(raw_img.content)
    img.seek(0)
    return img

def update_metadata(filename: str, metadata: dict):
    from mutagen.id3 import TIT2, TPE1, TPE2, TALB
    audio_file = File(filename)
    filetype = filename[filename.index('.'):]
    
    if filetype in [".ogg", ".opus", ".flac"]:
        audio_file['artist'] = metadata['artist']
        audio_file['album artist'] = metadata['album artist']
        audio_file['title'] = metadata['track']
        audio_file['album'] = metadata['album']
    elif filetype == '.mp3':
        audio_file['TPE1'] = TPE1(encoding=3, text=metadata['artist'])
        audio_file['TPE2'] = TPE2(encoding=3, text=metadata['album artist'])
        audio_file['TIT2'] = TIT2(encoding=3, text=metadata['track'])
        audio_file['TALB'] = TALB(encoding=3, text=metadata['album'])
        
    audio_file = add_image_cover(audio_file, img=get_image_cover(metadata['cover_url']))
    audio_file.save()
    
def add_image_cover(audio_file, img: None):
    filename = audio_file.filename
    filetype = filename[filename.index('.'):]
    if filetype in [".ogg", ".opus", ".flac"]:
        import base64, mutagen.flac
        picture = mutagen.flac.Picture()
        picture.data = img.read()
        if filetype == ".flac":
            audio_file.clear_pictures()
            audio_file.add_picture(picture)
        else:
            audio_file["metadata_block_picture"] = base64.b64encode(picture.write()).decode('utf-8')
    elif filetype == ".mp3":
        from mutagen.id3 import APIC
        audio_file.tags.add(APIC(encoding=3, type=3, desc='Cover', data=img.read()))
    return audio_file