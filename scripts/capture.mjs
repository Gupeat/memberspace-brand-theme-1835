import { createRequire } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';
import fs from 'node:fs';
import { spawnSync } from 'node:child_process';

const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const candidates = [
  path.join(REPO, 'node_modules', 'playwright-core', 'package.json'),
  path.join(REPO, 'node_modules', 'playwright', 'package.json'),
];
let chromium;
for (const manifest of candidates) {
  if (!fs.existsSync(manifest)) continue;
  try {
    chromium = createRequire(pathToFileURL(manifest).href)(
      manifest.includes('playwright-core') ? 'playwright-core' : 'playwright'
    ).chromium;
    break;
  } catch {}
}

function findBrowser() {
  const fromEnv = process.env.EDGE_PATH || process.env.CHROME_PATH;
  if (fromEnv && fs.existsSync(fromEnv)) return fromEnv;
  const local = process.env.LOCALAPPDATA || '';
  const candidates = process.platform === 'win32'
    ? [
        path.join(process.env['ProgramFiles(x86)'] || 'C:/Program Files (x86)', 'Microsoft/Edge/Application/msedge.exe'),
        path.join(process.env.ProgramFiles || 'C:/Program Files', 'Microsoft/Edge/Application/msedge.exe'),
        path.join(process.env.ProgramFiles || 'C:/Program Files', 'Google/Chrome/Application/chrome.exe'),
        path.join(local, 'Google/Chrome/Application/chrome.exe'),
      ]
    : process.platform === 'darwin'
      ? [
          '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
          '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        ]
      : [
          '/usr/bin/microsoft-edge',
          '/usr/bin/google-chrome',
          '/usr/bin/chromium',
          '/usr/bin/chromium-browser',
        ];
  return candidates.find((candidate) => candidate && fs.existsSync(candidate)) || null;
}

const BROWSER = findBrowser();
const OUT = path.join(REPO, 'artifacts', 'example-page.png');
const DEMO = path.join(REPO, 'demo', 'index.html');

if (!chromium && !BROWSER) {
  throw new Error('No Chromium/Edge/Chrome found. Install Playwright, or set EDGE_PATH/CHROME_PATH.');
}

if (!chromium) {
  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  const result = spawnSync(BROWSER, [
    '--headless=new', '--disable-gpu', '--hide-scrollbars',
    '--window-size=750,2261', `--screenshot=${OUT}`,
    pathToFileURL(DEMO).href,
  ], { encoding: 'utf8' });
  if (result.status !== 0 || !fs.existsSync(OUT)) {
    throw new Error('Edge headless capture failed: ' + (result.stderr || result.error || 'unknown'));
  }
  const png = fs.readFileSync(OUT);
  const width = png.readUInt32BE(16);
  const height = png.readUInt32BE(20);
  assert(width === 750, 'screenshot width is ' + width);
  assert(height >= 1500, 'screenshot height is ' + height);
  assert(png.length > 10000, 'screenshot too small: ' + png.length);
  console.log(JSON.stringify({ ok: true, mode: 'edge-cli', screenshot: 'artifacts/example-page.png', bytes: png.length, width, height }, null, 2));
  process.exit(0);
}

function assert(cond, message) { if (!cond) throw new Error(message); }

const browser = await chromium.launch(BROWSER ? { executablePath: BROWSER, headless: true } : { headless: true });
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