// Renders index.html frame-by-frame to MP4.  Usage: node render.mjs [out.mp4] [audio.wav]
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import { spawn } from 'node:child_process';
const OUT = process.argv[2] || 'intro.mp4', AUDIO = process.argv[3], FPS = 30, DUR = 26;
const args = ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-'];
if (AUDIO) args.push('-i', AUDIO, '-c:a', 'aac', '-b:a', '192k', '-shortest');
args.push('-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', OUT);
const ff = spawn('ffmpeg', args, { stdio: ['pipe', 'inherit', 'inherit'] });
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
p.on('pageerror', e => console.log('ERR', e.message));
await p.goto('file://' + process.cwd() + '/index.html?render');
await p.evaluate(() => window.READY);
// wait until the compositor has painted the new frame (heavy SVG layers can lag a frame)
const settle = () => p.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(() => setTimeout(r, 0)))));
// warm-up: paint every scene once so the first captured frame of each isn't half-drawn
for (const t of [1, 2.5, 3.2, 5, 9, 12.5, 16, 19.7, 22, 0]) { await p.evaluate(t => renderAt(t), t); await settle(); await p.screenshot({ type: 'jpeg', quality: 10 }); }
const total = FPS * DUR;
for (let i = 0; i < total; i++) {
  await p.evaluate(t => renderAt(t), i / FPS);
  await settle();
  const buf = await p.screenshot({ type: 'jpeg', quality: 95 });
  if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  if (i % 150 === 0) console.log(`frame ${i}/${total}`);
}
ff.stdin.end(); await b.close();
await new Promise(r => ff.on('close', r));
console.log('wrote', OUT);
