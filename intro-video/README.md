# Pull Up: intro video

30-second vertical (1080×1920, 30 fps) promo for Reels / TikTok / Shorts, built on the After Hours design system (Anton + Archivo, #0A0A0A / #FFC53D, gold brand gradient).

- `out/pullup-intro-1080x1920.mp4`: final cut with the synthesized 120 BPM track
- `out/pullup-intro-1080x1920-no-music.mp4`: same cut, silent, for adding trending audio in-app
- `index.html`: the animation itself. Open it in a browser to preview (space = play/pause, slider = scrub)

## Shot list
| Time | Shot |
|---|---|
| 0–2s | "WHERE'S EVERYONE TONIGHT?" type hook, gold wipe on the drop |
| 2–3s | Logo; it folds into a gold line that becomes the phone's edge |
| 3–7.5s | Phone swings open from side-on: **Discover** (live headcount, stories, Happening Now carousel) |
| 7.5–11s | Phone lies flat: **Map** with 3D pins rising off the screen |
| 11–17s | Push into the screen, pull out to a low side angle: **Event** → request → host approves |
| 17–22.5s | Whip pan to two phones: **New Party** + **Host dashboard** (live door counts) |
| 22.5–25.5s | Scan-line reveal of a wall of real screens: "PARTIES. FRIENDS. TICKETS. ONE APP." |
| 25.5–30s | End card: icon, wordmark, tagline, store buttons, handle |

## Editing
- Handle, tagline, city: `CONFIG` at the top of the `<script>` in `index.html` (the handle `@pullupapp` is a placeholder)
- Colors: the tokens at the top of the `<style>`
- Screens: `SCREENS` in `index.html`, laid out in 390×844 units like the design files

## Re-rendering
```
python3 music.py track.wav                                   # soundtrack (drop at 2.0s, cuts on the beat)
node render.mjs raw.mp4 track.wav                            # ~10 min, needs ffmpeg + playwright
ffmpeg -i raw.mp4 -c:v libx264 -crf 21 -c:a copy out.mp4     # shrink for upload
```
`node snap.mjs <dir> 5.2 8.9 …` saves stills at given seconds for quick checks.
