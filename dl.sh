# https://www.youtube.com/watch?v=EUoVXQgiW4w

# note: delete music mp3 beforehand
# create audio at music.mp3, thumbnail at music.mp3.png
yt-dlp -f "ba" -x --audio-format mp3 https://www.youtube.com/watch?v=EUoVXQgiW4w -o music.mp3 --write-thumbnail --convert-thumbnails png

# combine audio and video, output video at out.mp4
ffmpeg -y -i music.mp3 -loop 1 -i music.mp3.png -shortest -filter:a loudnorm -c:v libx264 -c:a aac out2.mp4
