#!/usr/bin/env bash
# Vertical 1080x1920 layout like the reference: banner, edited panel (with Hebrew captions) over the original panel.
# usage: layout.sh <v15 dir>
set -euo pipefail
d="$1"; F=/home/user/editing-tool/.claude/skills/hebrew-captions/fonts
ffmpeg -v error -y -i "$d/edited.mp4" -i "$d/out/rough.mp4" -i "$d/lay/banner.png" -i "$d/lay/orig.png" -filter_complex "
color=c=0x0F0F11:s=1080x1920:r=30[bg];
[0:v]subtitles=$d/captions.ass:fontsdir=$F,scale=1080:608:flags=lanczos,setsar=1[e];
[1:v]scale=1080:608:flags=lanczos,setsar=1[o];
[2:v]scale=760:-1:flags=lanczos[b];
[bg][e]overlay=0:372:shortest=1[x1];[x1][o]overlay=0:996[x2];[x2][b]overlay=(W-w)/2:150[x3];[x3][3:v]overlay=W-w-14:1004[v]" \
  -map "[v]" -map 1:a -c:v libx264 -preset medium -crf 10 -pix_fmt yuv420p -c:a aac -b:a 256k -r 30 "$d/layout.mp4"
ffprobe -v error -show_entries format=duration -of csv=p=0 "$d/layout.mp4"
