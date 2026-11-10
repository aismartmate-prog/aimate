#!/usr/bin/env python3
"""מחיל את עיצוב "סטודיו" (tools/subject-theme.css) על עמודי המקצוע.

הרצה:  python3 tools/apply-subject-theme.py math.html hebrew.html english.html arabic.html finance.html science.html
עובד גם על הקובץ המקורי וגם על עמוד שכבר עוצב (למשל אחרי שינוי ב-CSS) - הסקריפט
מחליף את השכבה הקודמת. לוגיקת העמוד (הסקריפטים, מאגרי הנושאים, הקישורים) לא משתנה:
כרטיסי הפעילות נשארים אותם אלמנטים בדיוק (onclick, id, style), רק מסודרים בפריסת בנטו.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CSS = open(os.path.join(HERE, 'subject-theme.css'), encoding='utf-8').read()
FONTS = 'https://fonts.googleapis.com/css2?family=Frank+Ruhl+Libre:wght@500;700;900&family=Heebo:wght@400;500;600;700;800;900&display=swap'
SUBJECTS = ['math', 'hebrew', 'english', 'arabic', 'finance', 'science']
SYMBOL = {'math': 'x²', 'hebrew': 'אב', 'english': 'Aa', 'arabic': 'ع', 'finance': '₪', 'science': 'H₂O'}
SIDE = ('learn', 'practice', 'quiz')          # הכרטיסים שבצד אריח הגיבור; כל השאר בשורה שמתחתיו

SCRIPT = '''<script>
    /* subject-theme: נגישות, וכפתור/אריח "ממשיכים מאיפה שעצרתם" לפי השיעורים האחרונים בדף הלמידה */
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

        var subj = document.body.getAttribute('data-subject') || '';
        function esc(s) { return String(s || '').replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
        var list = []; try { list = JSON.parse(localStorage.getItem('learnHistory') || '[]') || []; } catch (e) { }
        var last = list.filter(function (x) { return x && x.href && (x.href.indexOf('subject=' + subj) > -1 || x.href.indexOf('grade=' + subj) > -1); })[0];
        var passed = 0, started = 0;
        try { for (var i = 0; i < localStorage.length; i++) { var k = localStorage.key(i); if (k.indexOf('learnSeen|' + subj + '|') === 0) { started++; var v = JSON.parse(localStorage.getItem(k) || '{}'); if (v && v.__pass) passed++; } } } catch (e) { }
        var go = document.getElementById('studio-go'), tile = document.getElementById('studio-resume');
        function openLearn() { if (typeof openSelectionModal === 'function') openSelectionModal('למד אותי', true); }
        if (last) {
            go.outerHTML = '<a class="pill" id="studio-go" href="' + esc(last.href) + '"><i class="fa-solid fa-play" aria-hidden="true"></i><span>להמשיך: ' + esc(last.name) + '</span></a>';
            var pct = started ? Math.round(passed / started * 100) : 0;
            tile.outerHTML = '<a class="resume" id="studio-resume" href="' + esc(last.href) + '"><span class="go">להמשיך <i class="fa-solid fa-arrow-left"></i></span><span class="ring" style="--p:' + pct + '%"><b>' + passed + '/' + started + '</b></span><h3>' + esc(last.name) + '</h3><p>' + (passed ? 'שיעורים שעברתם את הבדיקה שלהם' : 'השיעור האחרון שפתחתם') + '</p></a>';
        } else {
            go.addEventListener('click', openLearn);
            tile.addEventListener('click', openLearn);
            tile.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openLearn(); } });
        }
    })();
</script>
'''


def take_element(src, start):
    """מחזיר את סוף אלמנט ה-div שמתחיל ב-start (ספירת div מאוזנת)."""
    depth, i = 0, start
    tag = re.compile(r'<(/?)div\b[^>]*>', re.I)
    for m in tag.finditer(src, start):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return m.end()
    raise ValueError('div לא סגור')


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

    # 3. פרטי הכותרת (מהמבנה המקורי או מהמעוצב)
    b = src.index('<body')
    c = re.search(r'<div class="container[^"]*">', src[b:])
    head_part, rest = src[b:b + c.start()], src[b + c.end():]
    grade = re.search(r'<p id="grade-display"[^>]*>(?:<i[^>]*></i>)?\s*(.*?)</p>', src[b:], re.S)
    grade = grade.group(1).strip() if grade else ''
    back = re.search(r'<a href="([^"]+)" class="back-btn">', head_part)
    back = back.group(1) if back else 'tirgul.html'
    w = re.search(r'\s*<div class="welcome-text">\s*<h2>(.*?)</h2>\s*<p>(.*?)</p>\s*</div>', rest, re.S)
    if w:
        title_src, sub = w.group(1), w.group(2).strip()
    else:
        title_src = re.search(r'<h1 class="board-title">(.*?)</h1>', src[b:], re.S).group(1)
        sub = re.search(r'<p class="board-sub">(.*?)</p>', src[b:], re.S).group(1).strip()
    icon = re.search(r'<i class="([^"]+)"[^>]*></i>', title_src)
    icon = icon.group(1) if icon else 'fa-solid fa-book'
    label = re.sub(r'<[^>]+>', '', title_src).strip()

    # 4. כרטיסי הפעילות - בדיוק כפי שהם, לפי הסדר
    modal = rest.index('<div id="selection-modal"')
    body_area, tail = rest[:modal], rest[modal:]
    cards = []
    for m in re.finditer(r'<div class="card [^"]*"', body_area):
        if cards and m.start() < cards[-1][1]:
            continue
        cards.append((m.start(), take_element(body_area, m.start())))
    html_cards = [body_area[s:e] for s, e in cards]
    def kind(h): return re.search(r'class="card ([\w-]+)', h).group(1)
    side = [h for h in html_cards if kind(h) in SIDE]
    row = [h for h in html_cards if kind(h) not in SIDE]

    header = f'''<body class="subj-{subj}" data-subject="{subj}">

<div id="floating-container" class="ambient-bg" aria-hidden="true"></div>

<header class="topbar"><div class="in">
    <a class="brand" href="{back}"><i class="fa-solid fa-graduation-cap" aria-hidden="true"></i><span>המרכז <em>להישגים</em></span></a>
    <a href="{back}" class="back-btn"><i class="fa-solid fa-house" aria-hidden="true"></i> לתפריט</a>
</div></header>

<div class="container content">
<div class="studio">
    <div class="studio-top">
        <section class="hero">
            <p id="grade-display" class="grade-chip">{grade}</p>
            <h1 class="board-title"><i class="{icon}" aria-hidden="true"></i><span>{label}</span></h1>
            <p class="board-sub">{sub}</p>
            <div class="hero-actions"><button type="button" class="pill" id="studio-go"><i class="fa-solid fa-play" aria-hidden="true"></i><span>פותחים שיעור</span></button></div>
            <div class="shapes" aria-hidden="true"><i class="s1"></i><i class="s2"></i><i class="s3"></i><b class="sym">{SYMBOL[subj]}</b></div>
        </section>
        <div class="studio-side">
        {(chr(10) + '        ').join(side)}
        </div>
    </div>
    <div class="studio-row">
        {(chr(10) + '        ').join(row)}
        <div class="resume" id="studio-resume" role="button" tabindex="0"><span class="go">לשיעור הראשון <i class="fa-solid fa-arrow-left"></i></span><span class="ring" style="--p:0%"><b>0</b></span><h3>ההתקדמות שלי</h3><p>עוד לא התחלתם שיעור במקצוע הזה</p></div>
    </div>
</div>
</div>

'''
    src = src[:b] + header + tail

    # 5. סקריפט עזר (נגישות + "ממשיכים מאיפה שעצרתם")
    src = re.sub(r'<script>\n    /\* subject-theme:.*?</script>\n', '', src, flags=re.S)
    k = src.rindex('</body>')
    src = src[:k] + SCRIPT + src[k:]
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
