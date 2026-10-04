# Pull Up: intro video

26-second vertical (1080×1920, 30 fps) promo for Reels / TikTok / Shorts, built from the real app screenshots in `shots/` and the After Hours design system (Anton + Archivo, #0A0A0A / #FFC53D).

- `out/pullup-intro-1080x1920.mp4`: final cut with the synthesized 120 BPM track
- `out/pullup-intro-1080x1920-no-music.mp4`: same cut, silent, for adding trending audio in-app
- `index.html`: the animation. Open it in a browser to preview (space = play/pause, slider = scrub)

## Shot list
One continuous phone, no hard cuts after the logo:

| Time | Shot |
|---|---|
| 0–2s | "WHERE'S EVERYONE TONIGHT?" |
| 2–3.5s | Logo on the drop; the icon opens into the app like an iOS app launch |
| 3.5–7s | "SEE WHO'S OUT TONIGHT": the real **Discover** screen, tap Map |
| 7–11s | "SWIPE THROUGH EVERY PARTY": the real **Map** screen; two swipes through the party cards, each party's pin answers |
| 11–15s | "THROWING ONE? POST IT": + → Create menu → Host a party → New Party form → Post |
| 15–18.5s | "LIVE ON THE MAP IN SECONDS": the new pin drops in, the carousel lands on the new party, guests count up |
| 18.5–21s | The phone turns to its side, then its back; the logo on the back becomes the end card |
| 21–26s | End card: icon, wordmark, tagline, store buttons |

## Screens
`shots/discover-src.jpg` and `shots/map-src.jpg` are the original screenshots. `./prep-shots.sh` turns them into what the video uses: it clears the status bars (the video draws a clean 9:41), removes the Map screen's bottom card strip so it can be rebuilt as live, swipeable cards, and crops the card thumbnails. To use new screenshots, replace the two `-src.jpg` files (same 734×1594 framing) and run it again.

## Editing
- Copy, and the party that gets posted: `CONFIG` at the top of the `<script>` in `index.html`
- Map cards: `CARDS`; pins: `PINS` (positions are in screenshot pixels)
- Timing: `PK` (phone camera), `carousel()`, `CAPS`

## Re-rendering
```
python3 music.py track.wav                                   # soundtrack (drop at 2.0s, cuts on the beat)
node render.mjs raw.mp4 track.wav                            # ~8 min, needs ffmpeg + playwright
ffmpeg -i raw.mp4 -c:v libx264 -crf 20 -c:a copy out.mp4     # shrink for upload
```
`node snap.mjs <dir> 8.65 15.9 …` saves stills at given seconds for quick checks.
