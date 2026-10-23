"""Build 02-ad-pro.html from its source: embed the site's fonts (Font Awesome) and point images at the screenshots.
usage: python3 motion/clips/tirgulim/gen.py"""
import base64, pathlib, re
HERE = pathlib.Path(__file__).resolve().parent
SITE = HERE.parents[1] / 'tirgulim' / 'site'
FA = SITE / 'npmfa' / 'package'
css = (FA / 'css' / 'all.min.css').read_text()
cp = lambda name: re.search(r"\.fa-" + name + r":before[^{]*\{content:\"\\([0-9a-f]+)\"", css).group(1)
ICONS = {'PENCIL': 'pencil', 'GRAD': 'graduation-cap', 'EXPAND': 'expand', 'CHECK': 'check', 'MIC': 'microphone',
         'CHART': 'chart-line', 'CALC': 'calculator', 'LANG': 'language', 'PEN': 'pen-nib', 'FLASK': 'flask-vial',
         'MOSQUE': 'mosque', 'COINS': 'coins', 'WA': 'whatsapp'}
b64 = lambda p: base64.b64encode(p.read_bytes()).decode()
fonts = (f"@font-face{{font-family:'FA6';font-weight:900;src:url(data:font/woff2;base64,{b64(FA/'webfonts'/'fa-solid-900.woff2')}) format('woff2')}}"
         f"@font-face{{font-family:'FA6B';font-weight:400;src:url(data:font/woff2;base64,{b64(FA/'webfonts'/'fa-brands-400.woff2')}) format('woff2')}}")
src = (HERE / '02-ad-pro.src.html').read_text(encoding='utf-8')
src = src.replace('/*FONTS*/', fonts).replace('SHOTS/', (SITE / 'shots').as_uri() + '/')
for tok in sorted(ICONS, key=len, reverse=True):
    src = re.sub(r'\b' + tok + r'\b', f'&#x{cp(ICONS[tok])};', src)
(HERE / '02-ad-pro.html').write_text(src, encoding='utf-8')
print('wrote', HERE / '02-ad-pro.html')
