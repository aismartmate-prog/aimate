#!/usr/bin/env python3
"""Adds the kids lesson-page look (tools/kids-learn-theme.css) to the kids learn.html, plus the owl in the banner.
Idempotent; page logic is untouched.  Usage: python3 tools/apply-kids-learn-theme.py learn.html [--out DIR]"""
import os, re, sys
here = os.path.dirname(os.path.abspath(__file__))
css = open(os.path.join(here, 'kids-learn-theme.css'), encoding='utf-8').read()
owl = open(os.path.join(here, '..', 'learn.html'), encoding='utf-8').read()
owl = owl[owl.index('<svg class="owl" id="owl"'):]; owl = owl[:owl.index('</svg>') + 6]
owl = re.sub(r'\s*<ellipse class="lid"[^\n]*\n', '\n', owl).replace('<svg class="owl" id="owl"', '<svg class="kl-owl"')
STYLE = '<style id="kids-learn-2026">\n' + css + '</style>\n'
JS = ('<script id="kids-learn-2026-js">\n(function () { var h = document.querySelector(".hero .in"); if (!h || h.querySelector(".kl-owl")) return;\n'
      '  var d = document.createElement("div"); d.innerHTML = ' + repr(owl.replace('\n', ' ')).replace('\\n', ' ') + '; h.appendChild(d.firstChild); })();\n</script>\n')
args = sys.argv[1:]; out = None
if '--out' in args:
    i = args.index('--out'); out = args[i + 1]; del args[i:i + 2]
for f in args:
    s = open(f, encoding='utf-8').read()
    s = re.sub(r'<style id="kids-learn-2026">.*?</style>\n', '', s, flags=re.S)
    s = re.sub(r'<script id="kids-learn-2026-js">.*?</script>\n', '', s, flags=re.S)
    i = s.index('</head>'); s = s[:i] + STYLE + s[i:]
    i = s.rfind('</body>'); s = s[:i] + JS + s[i:]
    dst = os.path.join(out, re.sub(r'_\d+\.html$', '.html', re.sub(r'^[0-9a-f]{8}-', '', os.path.basename(f)))) if out else f
    open(dst, 'w', encoding='utf-8').write(s); print('ok', dst)
