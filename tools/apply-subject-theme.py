#!/usr/bin/env python3
"""מחיל את עיצוב "הכיתה" (tools/subject-theme.css) על עמודי המקצוע.

הרצה:  python3 tools/apply-subject-theme.py math.html hebrew.html english.html arabic.html finance.html
אפשר להריץ שוב על עמוד שכבר עוצב (למשל אחרי שינוי ב-CSS) - הסקריפט מחליף את
השכבה הקודמת. לוגיקת העמוד (הסקריפטים, מאגרי הנושאים, הקישורים) לא משתנה.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CSS = open(os.path.join(HERE, 'subject-theme.css'), encoding='utf-8').read()
FONTS = 'https://fonts.googleapis.com/css2?family=Frank+Ruhl+Libre:wght@500;700;900&family=Rubik:wght@400;500;600;700;800;900&display=swap'
SUBJECTS = ['math', 'hebrew', 'english', 'arabic', 'finance', 'science']

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

    # 1. גופנים (את ה-viewport לא משנים: חסימת הזום מכוונת, נגד בעיית גלילה באנדרואיד)
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
    <div class="board">
        <p id="grade-display" class="grade-chip">{grade}</p>
        <h1 class="board-title"><i class="{icon}" aria-hidden="true"></i><span>{label}</span></h1>
        <span class="underline" aria-hidden="true"></span>
        <p class="board-sub">{sub}</p>
        <p class="board-tip"><i class="fa-solid fa-lightbulb" aria-hidden="true"></i><span>נושא חדש? מתחילים ב<b>למד אותי</b>, ואחר כך עוברים ל<b>תרגול</b>.</span></p>
    </div>
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
