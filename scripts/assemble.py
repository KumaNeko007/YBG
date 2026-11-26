#!/usr/bin/env python3
"""GitHub Actions step: join parts/index.html.partNNN byte-for-byte, verify SHA-256, write dist/index.html.

The parts are produced by tools/build_html.py from src/ (game.html + assets/).  Nothing here
edits the game: if a part is missing, renamed, re-encoded or changed, the build stops and the
currently published site stays as it is.
"""
from pathlib import Path
import hashlib
import re
import sys

src = Path('parts')
parts = sorted(src.glob('index.html.part*'))
if not parts:
    sys.exit('ERROR: no parts found in parts/')
numbers = []
for p in parts:
    m = re.fullmatch(r'index\.html\.part(\d{3})', p.name)
    if not m:
        sys.exit(f'ERROR: unexpected part name: {p.name}')
    numbers.append(int(m.group(1)))
if numbers != list(range(1, len(parts) + 1)):
    sys.exit(f'ERROR: missing or out-of-order parts: {numbers}')
raw = b''.join(p.read_bytes() for p in parts)
sha_file = src / 'index.html.sha256'
if not sha_file.exists():
    sys.exit('ERROR: parts/index.html.sha256 missing')
wanted = sha_file.read_text(encoding='ascii').split()[0].lower()
actual = hashlib.sha256(raw).hexdigest()
if actual != wanted:
    sys.exit(f'ERROR: sha256 mismatch: wanted {wanted}, got {actual}')
if not raw.startswith(b'<!DOCTYPE html>') or not raw.rstrip().endswith(b'</html>') or b'window.__ASSETS={' not in raw:
    sys.exit('ERROR: assembled file does not look like the game index.html')
out = Path('dist')
out.mkdir(exist_ok=True)
(out / 'index.html').write_bytes(raw)
for p in parts:
    print(f'{p.name}: {p.stat().st_size} bytes')
print(f'OK: dist/index.html {len(raw)} bytes, sha256 {actual}')
