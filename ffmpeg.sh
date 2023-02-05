ffmpeg \
    -hide_banner -loglevel error \
    -stream_loop -1 -i res/list.concat \
    -re -stream_loop -1 -i res/bg.mp4 \
    -filter_complex_script res/filter.txt \
    -map "[aout]" -map "[vout]" \
    -c:v libx264 -b:v 9M -maxrate 9M -bufsize 9M -c:a aac \
    -flush_packets 0 -f flv rtmp://lax.contribute.live-video.net/app
#    -flush_packets 0 -f rtsp -rtsp_transport tcp rtsp://localhost:8554/live.stream