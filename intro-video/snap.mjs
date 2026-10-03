import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const out = process.argv[2], times = process.argv.slice(3).map(Number);
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
p.on('console', m => console.log('console:', m.text())); p.on('pageerror', e => console.log('ERR', e.message));
await p.goto('file://' + process.cwd() + '/index.html?render');
await p.evaluate(() => window.READY);
for (const t of times) { await p.evaluate(t => renderAt(t), t); await p.screenshot({ path: `${out}/f_${t.toFixed(2)}.jpg`, quality: 80, type: 'jpeg' }); }
await b.close();
