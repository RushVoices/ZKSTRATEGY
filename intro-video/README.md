# Party app intro video

30-second vertical (1080×1920, 30 fps) promo for Reels / TikTok / Shorts.

- `out/intro-1080x1920.mp4`: final cut with the synthesized 120 BPM track
- `out/intro-1080x1920-no-music.mp4`: same cut, silent, for adding trending audio in-app
- `index.html`: the animation itself. Open it in a browser to preview (space = play/pause, slider = scrub)

## Rebranding
- App name, handle, tagline, city: `CONFIG` at the top of the `<script>` in `index.html`
- Colors: the `--c1`…`--c4` / `--bg` variables at the top of the `<style>`

## Re-rendering
```
python3 music.py track.wav                                       # optional soundtrack
node render.mjs out/intro-1080x1920.mp4 track.wav                # ~5 min, needs ffmpeg + playwright
ffmpeg -i out/intro-1080x1920.mp4 -c:v libx264 -crf 23 -c:a copy smaller.mp4   # shrink for upload
```
`node snap.mjs <dir> 4.3 11.5 …` saves stills at given seconds for quick checks.
