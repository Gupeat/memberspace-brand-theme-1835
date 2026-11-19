import { createRequire } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';
import fs from 'node:fs';

const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const candidates = [
  path.join(REPO, 'node_modules', 'playwright-core', 'package.json'),
  path.resolve(REPO, '..', '..', '2063', 'repo', 'package.json'),
];
let chromium;
for (const manifest of candidates) {
  if (!fs.existsSync(manifest)) continue;
  try {
    chromium = createRequire(pathToFileURL(manifest).href)('playwright-core').chromium;
    break;
  } catch {}
}
if (!chromium) throw new Error('playwright-core is required: run npm install playwright-core in this repo');

const EDGE = process.env.EDGE || 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const OUT = path.join(REPO, 'artifacts', 'example-page.png');
const DEMO = path.join(REPO, 'demo', 'index.html');

function assert(cond, message) { if (!cond) throw new Error(message); }

const browser = await chromium.launch({ executablePath: EDGE, headless: true });
try {
  const page = await browser.newPage({ viewport: { width: 750, height: 1400 }, deviceScaleFactor: 1 });
  await page.goto(pathToFileURL(DEMO).href, { waitUntil: 'load' });
  await page.waitForTimeout(400);
  const styles = await page.evaluate(() => {
    const read = (selector) => {
      const el = document.querySelector(selector);
      if (!el) return null;
      const cs = getComputedStyle(el);
      return { background: cs.backgroundColor, color: cs.color, font: cs.fontFamily, radius: cs.borderRadius };
    };
    return {
      title: document.title,
      button: read('[data-accent="button"]'),
      buttonLight: read('[data-accent="button-light"]'),
      tag: read('[data-accent="tag"]'),
      body: read('body'),
      appWidth: document.querySelector('[data-testid="app"]').getBoundingClientRect().width,
      height: document.documentElement.scrollHeight,
    };
  });
  assert(styles.button, 'primary button not found');
  assert(styles.tag, 'brand tag not found');
  assert(styles.button.background === 'rgb(31, 94, 255)', 'button background is ' + styles.button.background);
  assert(styles.tag.color === 'rgb(31, 94, 255)', 'tag text color is ' + styles.tag.color);
  assert(styles.tag.background === 'rgb(241, 244, 255)', 'tag background is ' + styles.tag.background);
  assert(styles.appWidth === 750, 'app width is ' + styles.appWidth);
  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  const shotHeight = await page.evaluate(() => document.documentElement.scrollHeight);
  await page.setViewportSize({ width: 750, height: shotHeight });
  await page.waitForTimeout(150);
  const png = await page.screenshot({ clip: { x: 0, y: 0, width: 750, height: shotHeight } });
  const pngWidth = png.readUInt32BE(16);
  const pngHeight = png.readUInt32BE(20);
  assert(pngWidth === 750, 'screenshot width is ' + pngWidth);
  assert(pngHeight >= 1500, 'screenshot height is ' + pngHeight);
  fs.writeFileSync(OUT, png);
  const bytes = png.length;
  assert(bytes > 10000, 'screenshot too small: ' + bytes);
  console.log(JSON.stringify({ ok: true, screenshot: 'artifacts/example-page.png', bytes, height: styles.height, button: styles.button.background, tag: styles.tag, appWidth: styles.appWidth }, null, 2));
} finally {
  await browser.close();
}
