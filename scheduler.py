import os
import subprocess
import playnext
import time
import random
import tbot
from multiprocessing import Process

song_queue = [
    ('https://www.youtube.com/watch?v=4fWyzwo1xg0', 'Simon & Garfunkel - The Sounds of Silence (Audio)', 186),
    # ('https://youtu.be/MtN1YnoL46Q', 'The duck song', 191),
    ('https://www.youtube.com/watch?v=I_izvAbhExY', 'Bee Gees - Stayin\' Alive (Official Video)', 249)
]

PRESET_SONGS = [
    'https://www.youtube.com/watch?v=SbSpDl40O3E',
    'https://www.youtube.com/watch?v=n3dNWEIG7vA',
    'https://www.youtube.com/watch?v=nsdDq258rRg',
    'https://www.youtube.com/watch?v=R1kOdTm9FBk',
    'https://www.youtube.com/watch?v=2Kff0U8w-aU',
    'https://www.youtube.com/watch?v=c75keT6Tm_g',
    'https://www.youtube.com/watch?v=K1PltwBuDKM',
    'https://www.youtube.com/watch?v=7m8ek8D9me0',
    'https://www.youtube.com/watch?v=jzJSd-vJ4y0',
    'https://www.youtube.com/watch?v=KbZJx5UVsw4',
    'https://www.youtube.com/watch?v=OIo0RbJLo8I',
    'https://www.youtube.com/watch?v=HO4DvFu32Yk',
    'https://www.youtube.com/watch?v=RXxxPiQ6WSU',
    'https://www.youtube.com/watch?v=gGwN25z7FrE',
    'https://www.youtube.com/watch?v=VjeoJ6I81vA',
    'https://www.youtube.com/watch?v=3cKtSlsYVEU',
    'https://www.youtube.com/watch?v=7xu_EBFR7dg',
    'https://www.youtube.com/watch?v=lJvRohYSrZM',
    'https://www.youtube.com/watch?v=fZ1pcOenxoo',
    'https://www.youtube.com/watch?v=recow3rW_qk',
    'https://www.youtube.com/watch?v=WVkD4lgXTEU'
]

processed_presets = [('https://www.youtube.com/watch?v=SbSpDl40O3E', 'My Resort', 133), ('https://www.youtube.com/watch?v=n3dNWEIG7vA', 'RAYE - Environmental Anxiety. (Visualizer)', 194), ('https://www.youtube.com/watch?v=nsdDq258rRg', 'Pongo - Wegue Wegue (Official London Video)', 220), ('https://www.youtube.com/watch?v=R1kOdTm9FBk', 'Party In The U.S.A.', 202), ('https://www.youtube.com/watch?v=2Kff0U8w-aU', 'OMG', 212), ('https://www.youtube.com/watch?v=c75keT6Tm_g', '夢中人', 261), ('https://www.youtube.com/watch?v=K1PltwBuDKM', 'Catch the Moment', 286), ('https://www.youtube.com/watch?v=7m8ek8D9me0', 'MIN - CÀ PHÊ | OFFICIAL MUSIC VIDEO', 213), ('https://www.youtube.com/watch?v=jzJSd-vJ4y0', 'Requiem, K. 626. Confutatis', 140), ('https://www.youtube.com/watch?v=KbZJx5UVsw4', 'Ta3ala Adalla3ak', 211), ('https://www.youtube.com/watch?v=OIo0RbJLo8I', 'Opa Opa', 214), ('https://www.youtube.com/watch?v=HO4DvFu32Yk', 'Voulez-Vous', 311), ('https://www.youtube.com/watch?v=RXxxPiQ6WSU', 'POPOPOP', 156), ('https://www.youtube.com/watch?v=gGwN25z7FrE', 'Anti-Hero', 201), ('https://www.youtube.com/watch?v=VjeoJ6I81vA', 'カワキヲアメク', 252), ('https://www.youtube.com/watch?v=3cKtSlsYVEU', 'September', 215), ('https://www.youtube.com/watch?v=7xu_EBFR7dg', 'Waka Waka (This Time for Africa)', 200), ('https://www.youtube.com/watch?v=lJvRohYSrZM', 'METAMORPHOSIS', 143), ('https://www.youtube.com/watch?v=fZ1pcOenxoo', 'Giant Steps', 283), ('https://www.youtube.com/watch?v=recow3rW_qk', 'Sea of Dreams', 283), ('https://www.youtube.com/watch?v=WVkD4lgXTEU', 'Bones in the Ocean', 194)]

def add_to_queue(link: str):
    song_queue.append(link)
    print(song_queue)

def get_rand_from_queue() -> str:
    if len(song_queue) <= 1:
        song_queue.append(processed_presets[random.randrange(len(processed_presets))])
        print('Adding bonus song', len(song_queue))
    print('curr song queue:', song_queue)
    return song_queue.pop(random.randrange(len(song_queue)))


def init_ffmpeg():
    subprocess.run('bash ffmpeg.sh', shell=True)

def init_bot():
    bot = tbot.Bot(add_to_queue, PRESET_SONGS, processed_presets)
    print(processed_presets)
    bot.run()


def main():
    # initialize everything, then enter song management loop

    with open('res/temp.nested.concat', 'w') as f:
        f.write('ffconcat version 1.0\nfile fallback.mp4')
        f.flush()
        os.fsync(f.fileno())
    os.replace('res/temp.nested.concat', 'res/nested.concat')

    ffmpeg = Process(target=init_ffmpeg)
    bot = Process(target=init_bot)

    ffmpeg.start()
    bot.start()

    time.sleep(5)
    print('Initialized.')

    playing_first = False
    playing_second = False
    now_playing = ('', '<downloading...>', 0)

    while True:
        start_time = time.time()

        # pick new song, swap displays
        next_song = get_rand_from_queue()

        # swap temp to next song
        with open('res/context_temp.txt', 'w') as f:
            f.write(next_song[1])
            f.flush()
            os.fsync(f.fileno())
        os.replace('res/context_temp.txt', 'res/context_next.txt')

        # while True:
        #     try:
        #         os.replace('res/context_temp.txt', 'res/context_next.txt')
        #     except Exception as e:
        #         print(e)
        #         print('trying to replace:', 'res/context_temp.txt', 'to', 'res/context_next.txt')

        # swap temp to cur song
        with open('res/context_temp.txt', 'w') as f:
            f.write(now_playing[1])
            f.flush()
            os.fsync(f.fileno())
        os.replace('res/context_temp.txt', 'res/context_cur.txt')

        # while True:
        #     try:
        #         os.replace('res/context_temp.txt', 'res/context_cur.txt')
        #     except Exception as e:
        #         print(e)
        #         print('trying to replace:', 'res/context_temp.txt', 'to', 'res/context_cur.txt')

        print('Queued:', next_song)

        # play next song if it's possible (ie, not initial loop around)
        if playing_first or playing_second:
            next_to_play = 'first' if playing_second else 'second'
            print(f'Playing next with {next_to_play}')
            playnext.play_next(next_to_play)

        # download next song
        if playing_second:
            print('Downloading', next_song, 'to second')
            playnext.dl_next(next_song, 'second')
        else:
            print('Downloading', next_song, 'to first')
            playnext.dl_next(next_song, 'first')

        print("Waiting for song to finish...")
        while int(time.time()-start_time) < now_playing[2]:
            time.sleep(1)
        print('Done waiting...')
        
        # next song!
        now_playing = next_song
        if playing_first:
            playing_first = False
            playing_second = True
        elif playing_second:
            playing_first = True
            playing_second = False
        else:
            playing_second = True



if __name__ ==  '__main__':
    main()



