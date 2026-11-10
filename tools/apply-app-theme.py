#!/usr/bin/env python3
"""מחיל את עיצוב "הכיתה" (tools/app-theme.css) על דפי התרגול והמבחן.

הרצה:  python3 tools/apply-app-theme.py practice.html exam.html
השכבה נכנסת כ-<style id="classroom-theme-2026"> בסוף ה-<head> (אחרי כל
שכבות העיצוב הקיימות). הרצה חוזרת מחליפה את השכבה הקודמת. הסקריפטים לא משתנים.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CSS = open(os.path.join(HERE, 'app-theme.css'), encoding='utf-8').read().strip()
TAG = '<style id="classroom-theme-2026">\n' + CSS + '\n</style>\n'


def apply(path):
    src = open(path, encoding='utf-8').read()
    src = re.sub(r'<style id="classroom-theme-2026">.*?</style>\n', '', src, count=1, flags=re.S)
    body = re.search(r'^<body[ >]', src, re.M)                  # תג ה-body האמיתי (לא בתוך מחרוזת JS)
    head_end = src.rindex('</head>', 0, body.start())
    src = src[:head_end] + TAG + src[head_end:]
    return src


if __name__ == '__main__':
    args = sys.argv[1:]
    out_dir = None
    if '--out' in args:
        k = args.index('--out'); out_dir = args[k + 1]; del args[k:k + 2]
    for p in args:
        html = apply(p)
        name = re.sub(r'^[0-9a-f]{8}-', '', os.path.basename(p)).replace('_2.html', '.html')
        dest = os.path.join(out_dir, name) if out_dir else p
        open(dest, 'w', encoding='utf-8').write(html)
        print('עוצב:', dest)
