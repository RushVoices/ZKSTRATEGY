#!/usr/bin/env bash
# Downloads a real street map (CARTO "Dark Matter" basemap, OpenStreetMap data) around
# Pacific Beach, San Diego and stitches it into map/map.png for the Map screen.
# Needs network access to basemaps.cartocdn.com.  Usage: ./fetch-map.sh [lat] [lon] [zoom]
set -euo pipefail
LAT=${1:-32.7960}; LON=${2:--117.2470}; Z=${3:-16}; STYLE=${STYLE:-dark_all}
cd "$(dirname "$0")"; mkdir -p map/tiles
read CX CY < <(python3 -c "
import math; lat,lon,z=$LAT,$LON,$Z; n=2**z
x=(lon+180)/360*n; y=(1-math.asinh(math.tan(math.radians(lat)))/math.pi)/2*n
print(int(x), int(y))")
COLS=4; ROWS=6; X0=$((CX-1)); Y0=$((CY-2))
inputs=(); layout=()
for r in $(seq 0 $((ROWS-1))); do for c in $(seq 0 $((COLS-1))); do
  x=$((X0+c)); y=$((Y0+r)); f=map/tiles/${Z}_${x}_${y}.png
  [ -s "$f" ] || curl -sSf -A "Mozilla/5.0" -o "$f" "https://a.basemaps.cartocdn.com/${STYLE}/${Z}/${x}/${y}@2x.png"
  inputs+=(-i "$f"); layout+=("$((c*512))_$((r*512))")
done; done
L=$(IFS='|'; echo "${layout[*]}")
# stitch 2048x3072, crop to the phone's 390:844 aspect at 3x (1170x2532)
ffmpeg -loglevel error -y "${inputs[@]}" -filter_complex "xstack=inputs=$((COLS*ROWS)):layout=$L,crop=1170:2532:439:270" map/map.png
echo "wrote map/map.png"
