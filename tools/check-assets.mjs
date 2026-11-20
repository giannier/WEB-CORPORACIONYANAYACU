#!/usr/bin/env node
/**
 * Verifies that every local asset referenced from dist/ exists (HTML src/href/srcset/data-settings URLs and CSS url()).
 * Also reports references to corporacionyanayacu.com (the clone must not depend on the live site).
 * Usage: npm run build && npm run check
 */
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const DIST = path.join(path.dirname(fileURLToPath(import.meta.url)), '..', 'dist');
const walk = d => fs.readdirSync(d, {withFileTypes: true}).flatMap(e => e.isDirectory() ? walk(path.join(d, e.name)) : [path.join(d, e.name)]);
const files = walk(DIST);
const missing = new Map();
let checked = 0;
const liveRefs = [];

function check(from, ref) {
  ref = ref.replace(/&amp;/g, '&').replace(/&#038;/g, '&').replace(/\\\//g, '/').trim();
  if (!ref || /^(#|data:|mailto:|tel:|javascript:|https?:|\/\/)/i.test(ref)) {
    if (/corporacionyanayacu.com/i.test(ref) && !/^https?:\/\/rrhh\.corporacionyanayacu.com/i.test(ref)) liveRefs.push(`${path.relative(DIST, from)} -> ${ref}`);
    return;
  }
  const clean = ref.split(/[?#]/)[0];
  if (!clean) return;
  let target = path.resolve(path.dirname(from), clean);
  checked++;
  if (fs.existsSync(target) && fs.statSync(target).isDirectory()) target = path.join(target, 'index.html');
  if (!fs.existsSync(target)) missing.set(`${path.relative(DIST, from)} -> ${ref}`, true);
}

for (const f of files) {
  const ext = path.extname(f);
  if (ext === '.css') {
    const t = fs.readFileSync(f, 'utf8');
    for (const m of t.matchAll(/url\(\s*['"]?([^'")]+?)['"]?\s*\)/g)) check(f, m[1]);
    for (const m of t.matchAll(/https?:\/\/corporacionyanayacu.com[^\s'")]*/g)) liveRefs.push(`${path.relative(DIST, f)} -> ${m[0]}`);
  } else if (ext === '.html') {
    const t = fs.readFileSync(f, 'utf8');
    for (const m of t.matchAll(/\b(?:src|href|poster|data-src)=["']([^"']+)["']/g)) check(f, m[1]);
    for (const m of t.matchAll(/\bsrcset=["']([^"']+)["']/g)) for (const p of m[1].split(',')) check(f, p.trim().split(/\s+/)[0]);
    // URLs inside JSON (data-settings): "url":"./assets/..." or "..\/assets\/..."
    for (const m of t.matchAll(/(?:&quot;|")url(?:&quot;|")\s*:\s*(?:&quot;|")([^"&]+?)(?:&quot;|")/g)) check(f, m[1]);
    for (const m of t.matchAll(/https?:\/\/(?:www\.)?corporacionyanayacu.com[^\s'"<)]*/g)) liveRefs.push(`${path.relative(DIST, f)} -> ${m[0]}`);
  }
}

console.log(`Checked ${checked} local references in ${files.length} files.`);
if (liveRefs.length) { console.log(`\nReferences to the live site (${liveRefs.length}):`); [...new Set(liveRefs)].forEach(r => console.log('  ' + r)); }
if (missing.size) { console.log(`\nMISSING (${missing.size}):`); [...missing.keys()].forEach(r => console.log('  ' + r)); process.exitCode = 1; }
else console.log('No missing assets.');
