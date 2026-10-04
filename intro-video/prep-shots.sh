#!/usr/bin/env bash
# Builds the screen images the video uses from the real app screenshots in shots/:
#   discover-src.jpg / map-src.jpg (734x1594 iPhone screenshots)
# Outputs (shots/): discover.png, map.png (status bar cleared; map card strip removed so the
# carousel can be rebuilt as live, swipeable cards), thumb-*.jpg and cover.jpg.
set -euo pipefail
cd "$(dirname "$0")/shots"
F="ffmpeg -loglevel error -y"

# The screenshots carry a thin gray frame; the real screen is the 729x1582 area at (2,12).
# Coordinates below are in the uncropped source; index.html maps them with (x-2, y-12).
CROP="crop=729:1582:2:12"

# Discover: clear the status bar (time + live-activity pill) — the video draws a clean 9:41 bar
$F -i discover-src.jpg -vf "format=rgb24,drawbox=x=0:y=22:w=734:h=92:color=0x0a0a0a:t=fill,$CROP" discover.png

# Map: clear status text over the water, then replace the bottom card strip (y 1155–1434)
# with a blurred reflection of the map just above it, faded under the cards.
$F -i map-src.jpg -filter_complex "
  [0]format=rgba,drawbox=x=60:y=40:w=150:h=66:color=0x0a1522:t=fill,split[m0][sb];
  [sb]split[sb1][sb2];
  [sb1]crop=170:24:527:98[f1];
  [sb2]crop=170:24:521:98[f2];
  [m0][f1]overlay=515:50:format=rgb[m0a];
  [m0a][f2]overlay=515:73:format=rgb[m1];
  [m1]split=3[base][s1][s2];
  [s1]crop=92:100:518:1050[fill];
  [s2]crop=734:200:0:955[band0];
  [band0][fill]overlay=612:95:format=rgb[band];
  [band]split[b1][b2];
  [b1]vflip,boxblur=3:2[top];
  [b2]crop=734:80:0:0,boxblur=3:2[bot];
  [base][top]overlay=0:1155:format=rgb[t1];
  [t1][bot]overlay=0:1355:format=rgb[t2];
  color=c=0x0a0a0a:s=734x1594,format=rgba,geq=r=10:g=10:b=10:a='if(lt(Y,1435),255*0.82*clip((Y-1125)/90,0,1),0)'[scrim];
  [t2][scrim]overlay=0:0:format=rgb,format=rgb24,$CROP" -frames:v 1 map.png

# Card thumbnails (2x of the 154x185 card thumb) and the New Party cover
$F -i map-src.jpg      -vf "crop=154:185:99:1185,scale=308:370:flags=lanczos" -q:v 3 thumb-yes.jpg
$F -i discover-src.jpg -vf "crop=92:110:137:1300,scale=308:370:flags=lanczos" -q:v 3 thumb-kieran.jpg
$F -i discover-src.jpg -vf "crop=250:300:180:290,scale=308:370:flags=lanczos" -q:v 3 thumb-test.jpg
$F -i discover-src.jpg -vf "crop=250:300:45:300,scale=308:370:flags=lanczos" -q:v 3 thumb-new.jpg
$F -i discover-src.jpg -vf "crop=520:248:40:300" -q:v 3 cover.jpg
echo "shots ready"
