#!/usr/bin/env python3
"""Inject tools/home-theme.css into the home page (before the last </body>). Idempotent.
Usage: python3 tools/apply-home-theme.py tirgul.html [--out DIR]"""
import re, sys, os
here = os.path.dirname(os.path.abspath(__file__))
css = open(os.path.join(here, 'home-theme.css'), encoding='utf-8').read()
args = sys.argv[1:]; out = None
if '--out' in args:
    i = args.index('--out'); out = args[i + 1]; del args[i:i + 2]
block = '<style id="home-cards-2026">\n' + css + '</style>\n'
for f in args:
    s = open(f, encoding='utf-8').read()
    s = re.sub(r'<style id="home-cards-2026">.*?</style>\n', '', s, flags=re.S)
    i = s.rfind('</body>')
    s = s[:i] + block + s[i:]
    dst = os.path.join(out, os.path.basename(f)) if out else f
    open(dst, 'w', encoding='utf-8').write(s)
    print('ok', dst)
