#!/usr/bin/env python3
"""Inject tools/home-theme.css into the home page (at the end of <head>). Idempotent.
Usage: python3 tools/apply-home-theme.py tirgul.html [--kids] [--out DIR]"""
import re, sys, os
here = os.path.dirname(os.path.abspath(__file__))
css = open(os.path.join(here, 'home-theme.css'), encoding='utf-8').read()
args = sys.argv[1:]; out = None
kids = '--kids' in args
if kids:
    args.remove('--kids')
    css = css + open(os.path.join(here, 'home-kids-theme.css'), encoding='utf-8').read()
# @import must come first inside a <style> block
imports = re.findall(r"^@import[^\n]*\n", css, flags=re.M)
css = ''.join(imports) + re.sub(r"^@import[^\n]*\n", '', css, flags=re.M)
JS = open(os.path.join(here, 'home-theme.js.html'), encoding='utf-8').read().replace('__KIDS__', 'true' if kids else 'false')
block = '<style id="home-cards-2026">\n' + css + '</style>\n'
for f in args:
    s = open(f, encoding='utf-8').read()
    s = re.sub(r'<style id="home-cards-2026">.*?</style>\n', '', s, flags=re.S)
    # בתוך ה-<head>: כך העיצוב חל מהרגע הראשון, ולא רק אחרי שכל הדף (מעל 1MB) נטען
    b = re.search(r'^<body[ >]', s, re.M)
    i = s.rindex('</head>', 0, b.start())
    s = s[:i] + block + s[i:]
    s = re.sub(r'<script id="home-cards-2026-js">.*?</script>\n', '', s, flags=re.S)
    j = s.rfind('</body>'); s = s[:j] + JS + s[j:]
    dst = os.path.join(out, re.sub(r'_\d+\.html$', '.html', re.sub(r'^[0-9a-f]{8}-', '', os.path.basename(f)))) if out else f
    open(dst, 'w', encoding='utf-8').write(s)
    print('ok', dst)
