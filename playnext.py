import os
import shutil
import subprocess
import time

WORKING_DIR = 'res'
RESOURCE_DIR = 'res'
NESTED_PATH = 'res/nested.concat'
TEMP_NESTED_PATH = 'res/temp.nested.concat'
FALLBACK_PATH = 'fallback.mp4'

# assumes tmp already exists

def join_to_working(filename: str) -> str:
    return os.path.join(WORKING_DIR, filename).replace('\\', '/')

# IMPORTANT NOTE: it takes ~1/6 the time of the next song to download & process it!
def dl_next(song_tup, dl_to: str) -> bool:

    yt_link = song_tup[0]

    # ensure a fallback while we download
    with open(NESTED_PATH, 'w') as f:
        f.write(f'ffconcat version 1.0\nfile {FALLBACK_PATH}')

    music_next_name = 'music.first.mp4' if dl_to == 'first' else 'music.second.mp4'

    if os.path.exists(join_to_working("music.mp4")):
        os.remove(join_to_working("music.mp4"))
    print(f'Downloading {yt_link} to {join_to_working("music.mp4")}')
    subprocess.run(f'yt-dlp -f b --recode mp4 {yt_link} -o {join_to_working("music.mp4")}', shell=True)

    # download music and thumbnail
    # if os.path.exists(join_to_working("music.mp3")):
    #     os.remove(join_to_working("music.mp3"))
    # subprocess.run(f'yt-dlp -f "ba" -x --audio-format mp3 {yt_link} -o {join_to_working("music.mp3")}', shell=True)
    # subprocess.run(f'yt-dlp -x --audio-format mp3 {yt_link} -o {join_to_working("music.mp3")} --write-thumbnail --convert-thumbnails png', shell=True)

    # process files
    print('ffmpeging')
    subprocess.run(f'ffmpeg -hide_banner -y -i {join_to_working("music.mp4")} -filter:a loudnorm -c:v libx264 -c:a aac -pix_fmt yuv420p -ar 44100 -b:a 256000 -r 30 {join_to_working(music_next_name)}', shell=True)
    # subprocess.run(f'ffmpeg -hide_banner -y -i {join_to_working("music.mp3")} -loop 1 -i {join_to_working("music.mp3.png")} -shortest -filter:a loudnorm -c:v libx264 -c:a aac -pix_fmt yuv420p -ar 44100 -b:a 256000 -r 30 {join_to_working(music_next_name)}', shell=True)
    print('done ffmpeg')

# switch to next song
def play_next(next_to_play: str):
    # set playlist to next song
    music_next_name = 'music.first.mp4' if next_to_play == 'first' else 'music.second.mp4'
    with open(TEMP_NESTED_PATH, 'w') as f:
        f.write(f'ffconcat version 1.0\nfile {music_next_name}')
        f.flush()
        os.fsync(f.fileno())
    os.replace(TEMP_NESTED_PATH, NESTED_PATH)

    # while True:
    #     try:
    #         os.replace(TEMP_NESTED_PATH, NESTED_PATH)
    #     except Exception as e:
    #         print(e)
    #         print('trying to replace:', TEMP_NESTED_PATH, 'to', NESTED_PATH)


    time.sleep(5)

    # restore fallback
    with open(TEMP_NESTED_PATH, 'w') as f:
        f.write(f'ffconcat version 1.0\nfile fallback.mp4')
        f.flush()
        os.fsync(f.fileno())
    os.replace(TEMP_NESTED_PATH, NESTED_PATH)
    # while True:
    #     try:
    #         os.replace(TEMP_NESTED_PATH, NESTED_PATH)
    #     except Exception as e:
    #         print(e)
    #         print('trying to replace:', TEMP_NESTED_PATH, 'to', NESTED_PATH)


