from twitchio.ext import commands
import validator_collection
from urllib.parse import urlparse, parse_qs
import subprocess
from yt_dlp import YoutubeDL

# Queue for the YouTube Links
playlist = []

# Helper fn parsing out video ids
def video_id(value):
    query = urlparse(value)
    if query.hostname == 'youtu.be':
        return query.query[2:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail?
    return None


def valandaddsong(playlist, submission, af, otherList, addToList=False):
    # check if the submission is formatted as a link
    # returns True if valid url, else raises errors
    # if formatted as link
    if validator_collection.checkers.is_url(submission):
        # if the submission is a proper link, check that has domain youtube via parsing
        o = urlparse(submission)
        if bool((o.netloc.find('youtube.com') or o.netloc.find('youtu.be'))) and (True if o.path.find('playlist') == -1 else False):
                a = subprocess.run(f'yt-dlp -F  {submission} ', shell=True)
                if a.returncode == 0:
                    b = subprocess.run(f'yt-dlp --get-duration {submission} ', shell=True, capture_output=True)
                    durstring = b.stdout.decode("utf-8").rstrip()

                    if len(durstring.split(':')) == 3:
                        h, m, s = durstring.split(':')
                        timeinsec = int(h) * 3600 + int(m) * 60 + int(s)
                    elif len(durstring.split(':')) == 2:
                        m, s = durstring.split(':')
                        timeinsec = int(m) * 60 + int(s)
                    elif len(durstring.split(':')) == 1:
                        timeinsec = int(durstring)

                    if 360 >= timeinsec >= 90:
                        # af(f'https://youtube.com/watch?v={video_id(submission)}')
                        with YoutubeDL() as ydl:
                            info_dict = ydl.extract_info(submission, download=False)
                            finalreturn = (submission ,info_dict['title'], timeinsec) #link, name, leninsec
                            print('adding:', finalreturn)
                            if addToList:
                                otherList.append(finalreturn)
                            else:
                                af(finalreturn)

                        return 0  # if song is valid
                    else:
                        return -4  # if song is too long
                else:
                    return -3  # if not a valid youtube link
        else:
            return -2  # if link is a playlist
    else:
        return -1  # if not a link


class Bot(commands.Bot):

    def __init__(self, addFunc, presets, otherList):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        super().__init__(token='', prefix='!',
                         initial_channels=['realharmonyradio'])  # <-- Replace with your channel name

        self.addFunc = addFunc

        # for link in presets:
        #     valandaddsong([], link, self.addFunc, otherList, True)

    async def event_ready(self):
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        if message.echo:
            return

        print(message.content)
        await self.handle_commands(message)

        # Receives input after the command
        url = message.content
        url = url[8:]

        # Trims whitespace
        url.strip()
        print(url)

        # Playlist
        await message.channel.send('Processing request...', message.author)
        num = valandaddsong(playlist, url, self.addFunc, [])
        # Wrong input checking
        if '!' in message.content:
            if num == -1 and message.content != '!hello':
                await message.channel.send('Not a link')
            elif num == -2 and message.content != '!hello':
                await message.channel.send('Not a playlist')
            elif num == -3 and message.content != '!hello':
                await message.channel.send('Not a valid YouTube link')
            elif num == -4 and message.content != '!hello':
                await message.channel.send('Song is too long')
            else:
                if message.content != '!hello':
                    await message.channel.send('Song Received!')

    # !hello command
    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send(f'Hello {ctx.author.name}!')

    # !submit command (!submit 'youtube link')
    @commands.command()
    async def submit(self, ctx: commands.Context):
        num = valandaddsong(playlist, url, self.addFunc, [])
        # Wrong input checking
        if '!' in message.content:
            if num == -1 and message.content != '!hello':
                await message.channel.send('Not a link')
            elif num == -2 and message.content != '!hello':
                await message.channel.send('Not a playlist')
            elif num == -3 and message.content != '!hello':
                await message.channel.send('Not a valid YouTube link')
            elif num == -4 and message.content != '!hello':
                await message.channel.send('Song is too long')
            else:
                if message.content != '!hello':
                    await message.channel.send('Song Received!')

    # !info command
    @commands.command()
    async def info(self, ctx: commands.Context):
        await ctx.send(
            'Thank you for using InfiniBot! To use the bot, type in chat \'!submit <YouTube Link>\' '
            'For more information please visit our website at '
        )

