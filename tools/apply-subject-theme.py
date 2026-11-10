#!/usr/bin/env python3
"""מחיל את עיצוב "הכיתה" (tools/subject-theme.css) על עמודי המקצוע.

הרצה:  python3 tools/apply-subject-theme.py math.html hebrew.html english.html arabic.html finance.html
אפשר להריץ שוב על עמוד שכבר עוצב (למשל אחרי שינוי ב-CSS) - הסקריפט מחליף את
השכבה הקודמת. לוגיקת העמוד (הסקריפטים, מאגרי הנושאים, הקישורים) לא משתנה.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CSS = open(os.path.join(HERE, 'subject-theme.css'), encoding='utf-8').read()
FONTS = 'https://fonts.googleapis.com/css2?family=Amatic+SC:wght@700&family=Rubik:wght@400;500;600;700;800;900&display=swap'
SUBJECTS = ['math', 'hebrew', 'english', 'arabic', 'finance']

OWL = '''<svg class="owl" viewBox="0 0 200 215" aria-hidden="true">
            <ellipse cx="62" cy="205" rx="20" ry="8" fill="#f59f00"/><ellipse cx="138" cy="205" rx="20" ry="8" fill="#f59f00"/>
            <polygon points="42,58 52,22 78,50" fill="#7a4a24"/><polygon points="158,58 148,22 122,50" fill="#7a4a24"/>
            <ellipse cx="100" cy="128" rx="76" ry="82" fill="#9a6235"/>
            <ellipse cx="26" cy="140" rx="16" ry="44" fill="#7a4a24" transform="rotate(12 26 140)"/><ellipse cx="174" cy="140" rx="16" ry="44" fill="#7a4a24" transform="rotate(-12 174 140)"/>
            <ellipse cx="100" cy="152" rx="48" ry="52" fill="#f6dfb8"/>
            <path d="M78 150 q8 8 16 0 M106 150 q8 8 16 0 M92 168 q8 8 16 0" fill="none" stroke="#d9b98a" stroke-width="3" stroke-linecap="round"/>
            <circle cx="70" cy="96" r="29" fill="#fff"/><circle cx="130" cy="96" r="29" fill="#fff"/>
            <circle cx="74" cy="98" r="12" fill="#1b2440"/><circle cx="126" cy="98" r="12" fill="#1b2440"/>
            <circle cx="78" cy="93" r="4" fill="#fff"/><circle cx="130" cy="93" r="4" fill="#fff"/>
            <ellipse class="lid" cx="70" cy="96" rx="29" ry="29" fill="#9a6235"/><ellipse class="lid" cx="130" cy="96" rx="29" ry="29" fill="#9a6235"/>
            <circle cx="70" cy="96" r="31" fill="none" stroke="#1b2440" stroke-width="5"/><circle cx="130" cy="96" r="31" fill="none" stroke="#1b2440" stroke-width="5"/>
            <path d="M99 94 h2" stroke="#1b2440" stroke-width="5"/>
            <polygon points="100,108 90,122 110,122" fill="#f59f00"/>
            <polygon points="48,44 100,24 152,44 100,64" fill="#1b2440"/><rect x="78" y="50" width="44" height="14" rx="4" fill="#1b2440"/>
            <path d="M152 44 v26" stroke="#ffc93c" stroke-width="4"/><circle cx="152" cy="74" r="6" fill="#ffc93c"/>
        </svg>'''

# נגישות: הכרטיסים הם div עם onclick - הופכים אותם לכפתורים שאפשר להפעיל גם מהמקלדת
A11Y = '''<script>
    /* subject-theme: נגישות לכרטיסים ולחלון הבחירה */
    (function () {
        document.querySelectorAll('.card[onclick]').forEach(function (c) {
            c.setAttribute('role', 'button'); c.setAttribute('tabindex', '0');
            c.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); c.click(); } });
        });
        document.addEventListener('keydown', function (e) {
            var m = document.getElementById('selection-modal');
            if (e.key === 'Escape' && m && m.style.display === 'flex' && typeof closeModal === 'function') closeModal();
        });
        var m = document.getElementById('selection-modal');
        if (m) m.addEventListener('click', function (e) { if (e.target === m && typeof closeModal === 'function') closeModal(); });
        new MutationObserver(function () {
            document.querySelectorAll('.close-modal:not([role])').forEach(function (x) { x.setAttribute('role', 'button'); x.setAttribute('tabindex', '0'); x.setAttribute('aria-label', 'סגירה');
                x.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); x.click(); } }); });
        }).observe(document.body, { childList: true, subtree: true });
    })();
</script>
'''


def apply(path):
    src = open(path, encoding='utf-8').read()
    name = os.path.basename(path).lower()
    subj = next((s for s in SUBJECTS if s in name), None)
    if not subj:
        raise SystemExit('לא זוהה מקצוע בשם הקובץ: ' + path)

    # 1. viewport נגיש (מאפשר הגדלה) + גופנים
    src = re.sub(r'<meta name="viewport"[^>]*>', '<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">', src, count=1)
    src = re.sub(r'https://fonts\.googleapis\.com/css2\?[^"]+', FONTS, src)

    # 2. גיליון העיצוב
    i, j = src.index('<style>'), src.index('</style>')
    src = src[:i] + '<style>\n' + CSS.rstrip() + '\n    ' + src[j:]

    # 3. כותרת: הלוח והמורה, במקום ה-header והברכה הישנים
    b = src.index('<body')
    c = re.search(r'<div class="container[^"]*">', src[b:])
    head_part, rest = src[b:b + c.start()], src[b + c.end():]
    grade = re.search(r'<p id="grade-display"[^>]*>(.*?)</p>', head_part, re.S)
    grade = grade.group(1).strip() if grade else ''
    back = re.search(r'<a href="([^"]+)" class="back-btn">', head_part)
    back = back.group(1) if back else 'tirgul.html'
    title_src = head_part
    w = re.search(r'\s*<div class="welcome-text">\s*<h2>(.*?)</h2>\s*<p>(.*?)</p>\s*</div>', rest, re.S)
    if w:
        title_src = w.group(1); sub = w.group(2).strip(); rest = rest[:w.start()] + rest[w.end():]
    else:
        t = re.search(r'<h1 class="board-title">(.*?)</h1>', head_part, re.S); title_src = t.group(1)
        s = re.search(r'<p class="board-sub">(.*?)</p>', head_part, re.S); sub = s.group(1).strip()
    icon = re.search(r'<i class="([^"]+)"[^>]*></i>', title_src)
    icon = icon.group(1) if icon else 'fa-solid fa-book'
    label = re.sub(r'<[^>]+>', '', title_src).strip()

    header = f'''<body class="subj-{subj}">

<div id="floating-container" class="ambient-bg" aria-hidden="true"></div>

<header class="topbar"><div class="in">
    <a class="brand" href="{back}"><i class="fa-solid fa-chalkboard-user" aria-hidden="true"></i><span>המרכז להישגים לימודיים</span></a>
    <a href="{back}" class="back-btn"><i class="fa-solid fa-house" aria-hidden="true"></i> לתפריט</a>
</div></header>

<section class="classroom"><div class="in">
    <div class="board-wrap">
        <div class="board">
            <p id="grade-display" class="grade-chip">{grade}</p>
            <h1 class="board-title"><i class="{icon}" aria-hidden="true"></i><span>{label}</span></h1>
            <svg class="underline" viewBox="0 0 300 12" preserveAspectRatio="none" aria-hidden="true"><path d="M4 7 C 60 1, 110 11, 160 6 S 250 2, 296 8"/></svg>
            <p class="board-sub">{sub}</p>
        </div>
        <div class="tray" aria-hidden="true"></div>
    </div>
    <aside class="teacher" aria-label="המורה יוני">
        <div class="bubble">שלום! אני <b>יוני</b>. בחרו פעילות. נושא חדש? מתחילים ב<b>למד אותי</b> - ואחר כך <b>תרגול</b>.</div>
        {OWL}
    </aside>
</div></section>

<div class="container content">'''
    src = src[:b] + header + rest

    # 4. סמל לכותרת המשחקים
    src = re.sub(r'<h2 class="section-title(?: games)?">(למידה משחקית)', r'<h2 class="section-title games">\1', src)

    # 5. נגישות
    src = re.sub(r'<script>\n    /\* subject-theme:.*?</script>\n', '', src, flags=re.S)
    k = src.rindex('</body>')
    src = src[:k] + A11Y + src[k:]
    return src


if __name__ == '__main__':
    out_dir = None
    args = sys.argv[1:]
    if '--out' in args:
        k = args.index('--out'); out_dir = args[k + 1]; del args[k:k + 2]
    for p in args:
        html = apply(p)
        dest = os.path.join(out_dir, re.sub(r'^[0-9a-f]{8}-', '', os.path.basename(p))) if out_dir else p
        open(dest, 'w', encoding='utf-8').write(html)
        print('עוצב:', dest)
