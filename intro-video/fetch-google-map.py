#!/usr/bin/env python3
"""Builds map/map.png from the Google Maps Static API, styled to match Pull Up's dark UI.

Needs GOOGLE_MAPS_API_KEY in the environment (a key with the "Maps Static API" enabled).
Usage: python3 fetch-google-map.py [lat] [lon] [zoom]     (default: Pacific Beach, San Diego)

The phone screen is tall (390x844), so it stitches three 640x640@2x images vertically,
trimming the Google logo/credit off each one, then saves that credit strip separately as
map/credit.png. index.html shows the strip on the map, as Google's terms require.
"""
import math, os, subprocess, sys, urllib.parse
key = os.environ.get("GOOGLE_MAPS_API_KEY") or sys.exit("Set GOOGLE_MAPS_API_KEY first.")
lat, lon, z = (float(sys.argv[1]) if len(sys.argv) > 1 else 32.7960,
               float(sys.argv[2]) if len(sys.argv) > 2 else -117.2470,
               int(sys.argv[3]) if len(sys.argv) > 3 else 16)
here = os.path.dirname(os.path.abspath(__file__)); out = os.path.join(here, "map"); os.makedirs(out, exist_ok=True)

STYLE = [  # After Hours palette
    "element:geometry|color:0x141414", "element:labels.icon|visibility:off",
    "element:labels.text.fill|color:0x8d8a84", "element:labels.text.stroke|color:0x0a0a0a",
    "feature:administrative|element:geometry|visibility:off", "feature:poi|visibility:off", "feature:transit|visibility:off",
    "feature:poi.park|visibility:on", "feature:poi.park|element:geometry|color:0x15190f", "feature:poi.park|element:labels|visibility:off",
    "feature:road|element:geometry.fill|color:0x262626", "feature:road|element:geometry.stroke|color:0x141414",
    "feature:road.arterial|element:geometry.fill|color:0x2e2e2e", "feature:road.highway|element:geometry.fill|color:0x3a3a3a",
    "feature:road.local|element:labels|visibility:simplified",
    "feature:water|element:geometry|color:0x0b1118", "feature:water|element:labels.text.fill|color:0x3d4a5a",
]
def latlon_to_px(la, lo):
    n = 256 * 2 ** z
    return (lo + 180) / 360 * n, (1 - math.asinh(math.tan(math.radians(la))) / math.pi) / 2 * n
def px_to_lat(y):
    n = 256 * 2 ** z
    return math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n))))

cx, cy = latlon_to_px(lat, lon)
STEP = 600                      # logical px between strip centers; each strip keeps its top 600px (1200 at @2x)
files = []
for i in range(3):
    la = px_to_lat(cy + (i - 1) * STEP)
    q = [("center", f"{la:.6f},{lon:.6f}"), ("zoom", z), ("size", "640x640"), ("scale", 2), ("format", "png"), ("key", key)]
    q += [("style", s) for s in STYLE]
    f = os.path.join(out, f"g{i}.png")
    subprocess.run(["curl", "-sSf", "-o", f, "https://maps.googleapis.com/maps/api/staticmap?" + urllib.parse.urlencode(q)], check=True)
    files.append(f)

# stack the top 1200px of each strip (3600 tall), crop to the phone aspect 1280x2770; keep the bottom 80px of the last strip as the credit
args = ["ffmpeg", "-loglevel", "error", "-y"] + sum([["-i", f] for f in files], [])
graph = "".join(f"[{i}]crop=1280:1200:0:0[c{i}];" for i in range(3)) + "[c0][c1][c2]vstack=3,crop=1280:2770:0:415[m]"
subprocess.run(args + ["-filter_complex", graph, "-map", "[m]", os.path.join(out, "map.png")], check=True)
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", files[2], "-vf", "crop=1280:80:0:1200", os.path.join(out, "credit.png")], check=True)
for f in files: os.remove(f)
print("wrote map/map.png and map/credit.png")
