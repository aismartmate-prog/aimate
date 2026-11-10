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
KIDS_CSS = open(os.path.join(HERE, 'kids-theme.css'), encoding='utf-8').read()
KIDS_FONTS = FONTS.replace('&display=swap', '&family=Rubik:wght@400;500;700;800;900&display=swap')
OWL = '''<div class="owl-wrap" aria-hidden="true"><span class="owl-say">היי! בואו נלמד יחד</span>
<svg class="owl" viewBox="0 0 200 215" aria-hidden="true">
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
</svg>
</div>'''
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


def apply(path, kids=False):
    src = open(path, encoding='utf-8').read()
    name = os.path.basename(path).lower()
    subj = next((s for s in SUBJECTS if s in name), None)
    if not subj:
        raise SystemExit('לא זוהה מקצוע בשם הקובץ: ' + path)

    # 1. גופנים (את ה-viewport לא משנים: חסימת הזום מכוונת, נגד בעיית גלילה באנדרואיד)
    src = re.sub(r'https://fonts\.googleapis\.com/css2\?[^"]+', KIDS_FONTS if kids else FONTS, src)

    # 2. גיליון העיצוב
    i, j = src.index('<style>'), src.index('</style>')
    src = src[:i] + '<style>\n' + CSS.rstrip() + (KIDS_CSS.rstrip() if kids else '') + '\n    ' + src[j:]

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

    header = f'''<body class="subj-{subj}{' kids' if kids else ''}" data-subject="{subj}">

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
            <ol class="hero-path" aria-label="איך לומדים כאן"><li class="cap">המסלול המומלץ</li><li><b>1</b><span>למד אותי<small>שיעור מסודר על הנושא</small></span></li><li><b>2</b><span>תרגול<small>עם רמזים ופתרון מלא</small></span></li><li><b>3</b><span>בוחן או מבחן<small>בודקים שזה יושב</small></span></li></ol>
            {OWL if kids else '<div class="shapes" aria-hidden="true"><i class="s1"></i><i class="s2"></i><i class="s3"></i><b class="sym">' + SYMBOL[subj] + '</b></div>'}
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
    kids = '--kids' in args
    if kids: args.remove('--kids')
    if '--out' in args:
        k = args.index('--out'); out_dir = args[k + 1]; del args[k:k + 2]
    for p in args:
        html = apply(p, kids)
        dest = os.path.join(out_dir, re.sub(r'_\d+\.html$', '.html', re.sub(r'^[0-9a-f]{8}-', '', os.path.basename(p)))) if out_dir else p
        open(dest, 'w', encoding='utf-8').write(html)
        print('עוצב:', dest)
